# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import BooleanField
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DateField
from django.forms import DecimalField
from django.forms import ModelChoiceField
from django.forms import ModelMultipleChoiceField
from django.forms import MultipleChoiceField
from django.forms import ValidationError
from core.forms import MoneypitForm
from core.logic import is_conversion_needed
from core.logic.transaction import get_category_amounts
from core.logic.transaction import get_converted_amount_transfer
from core.models import Account
from core.models import AccountSplit
from core.models import Category
from core.models import CategorySplit
from core.models import Tag
from core.models import TagSplit
from core.models import Transaction
from core.models import Wealth
from logging import getLogger

logger = getLogger('core')


class TransactionAddForm(MoneypitForm):
  type = ChoiceField(choices=Transaction.TYPES)
  description = CharField(required=False)
  amount = DecimalField(initial=0.0)
  date = DateField(initial=datetime.utcnow())

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    self.accounts_list = kwargs.pop('accounts_list', None)
    super(TransactionAddForm, self).__init__(*args, **kwargs)
    self.fields['account_from'] = ChoiceField(choices=self.accounts_list)

  def clean_account_from(self):
    return self._check_account(
        'account_from',
        'The transaction account does not exist')

  def clean_amount(self):
    return self._check_amount('amount')

  def _check_account(self, field, error_msg):
    account_id = self.cleaned_data[field]
    try:
      Account.objects.get(id=account_id, wealth=self.wealth)
    except ObjectDoesNotExist:
      raise ValidationError(error_msg)
    return account_id

  def _check_amount(self, field):
    amount = self.cleaned_data[field]
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount


class TransactionAddNonTransferForm(TransactionAddForm):
  def __init__(self, *args, **kwargs):
    categories_list = kwargs.pop('categories_list', None)
    tag_list = kwargs.pop('tag_list', None)
    super(TransactionAddNonTransferForm, self).__init__(*args, **kwargs)

    self.fields['category_id'] = ChoiceField(choices=categories_list)
    self.fields['tags'] = MultipleChoiceField(
        choices=tag_list,
        required=False)

  def clean_category_id(self):
    category_id = self.cleaned_data['category_id']
    return int(category_id)

  def clean(self):
    super(TransactionAddNonTransferForm, self).clean()
    cleaned_data = self.cleaned_data

    if not 'date' in cleaned_data:
      self.add_error('date', 'Date is a compulsory argument')

    if not 'account_from' in cleaned_data:
      self.add_error('account_from', 'Account is a compulsory argument')

    account = Account.objects.get(
      wealth=self.wealth,
      id=cleaned_data['account_from'])

    if 'category_id' in cleaned_data and not cleaned_data['category_id']:
      self.add_error('category_id', 'Category is a compulsory argument')

    if cleaned_data['date'] < account.opened_date:
      self.add_error(
          'date',
          'Transaction cannot be made before the account existed')
    return cleaned_data

  def save(self):
    transaction_type = int(self.cleaned_data['type'])
    date = self.cleaned_data['date']
    description = self.cleaned_data['description']

    transaction = Transaction(
        date=date,
        description=description,
        type=transaction_type,
        wealth=self.wealth)
    transaction.save()

    account_from = Account.objects.get(
        wealth=self.wealth,
        id=self.cleaned_data['account_from'])

    amount = self.cleaned_data['amount']
    date = self.cleaned_data['date']
    tags = self.cleaned_data['tags']
    transaction_type = int(self.cleaned_data['type'])

    category = Category.objects.get(
        wealth=self.wealth,
        id=self.cleaned_data['category_id'])

    amount_account, amount_category = get_category_amounts(
        account_from,
        self.wealth,
        amount,
        transaction_type)

    split_account = AccountSplit(
        account=account_from,
        date=date,
        wealth=self.wealth,
        transaction=transaction,
        type=transaction_type,
        amount=amount_account)
    split_category = CategorySplit(
        wealth=self.wealth,
        date=date,
        category=category,
        type=transaction_type,
        transaction=transaction,
        amount=amount_category)

    split_account.save()
    split_category.save()

    if tags:
      for tag_id in tags:
        tag = Tag.objects.get(
            wealth=self.wealth,
            id=tag_id)
        tag_split = TagSplit(
            tag=tag,
            date=date,
            wealth=self.wealth,
            amount=amount_account,
            transaction=transaction,
            type=transaction_type)
        tag_split.save()
    return transaction


class TransactionAddTransferForm(TransactionAddForm):
  final = CharField(required=False)
  rate = CharField(required=False)

  def __init__(self, *args, **kwargs):
    super(TransactionAddTransferForm, self).__init__(*args, **kwargs)
    self.fields['account_id'] = ChoiceField(choices=self.accounts_list)

  def clean_final(self):
    return self._check_amount('final')

  def clean_rate(self):
    return self._check_amount('rate')

  def clean_account_id(self):
    account_id = self.cleaned_data['account_id']
    return int(account_id)

  def clean(self):
    super(TransactionAddTransferForm, self).clean()
    cleaned_data = self.cleaned_data

    if not 'date' in cleaned_data:
      self.add_error('date', 'Date is a compulsory argument')

    if not 'account_from' in cleaned_data:
      self.add_error('account_from', 'Account is a compulsory argument')

    account = Account.objects.get(
      wealth=self.wealth,
      id=cleaned_data['account_from'])

    if not cleaned_data['account_id']:
      self.add_error('account_id', 'Destination account is a compulsory argument')

    account_to = Account.objects.get(
      wealth=self.wealth,
      id=cleaned_data['account_id'])

    if account == account_to:
      self.add_error('account_id', 'Cannot transfer to itself')

    if cleaned_data['date'] < account_to.opened_date:
      self.add_error('date', 'Destination account did not exist')

    if is_conversion_needed(account, account_to):
      if 'rate' not in cleaned_data or 'final' not in cleaned_data:
        self.add_error('rate', 'Rate and final must be present in request')
      if cleaned_data['rate'] and cleaned_data['final']:
        self.add_error('rate', 'Specify rate OR final amount, not both')
        self.add_error('final', 'Specify rate OR final amount, not both')
      if not cleaned_data['rate'] and not cleaned_data['final']:
        self.add_error('rate', 'One of the fields is required')

    if cleaned_data['date'] < account.opened_date:
      self.add_error(
          'date',
          'Transaction cannot be made before the account existed')
    return cleaned_data

  def save(self):
    transaction_type = int(self.cleaned_data['type'])
    date = self.cleaned_data['date']
    description = self.cleaned_data['description']

    transaction = Transaction(
        date=date,
        description=description,
        type=transaction_type,
        wealth=self.wealth)
    transaction.save()

    account_from = Account.objects.get(
        wealth=self.wealth,
        id=self.cleaned_data['account_from'])

    amount = self.cleaned_data['amount']
    final = self.cleaned_data['final']
    rate = self.cleaned_data['rate']
    date = self.cleaned_data['date']
    transaction_type = int(self.cleaned_data['type'])

    account_to = Account.objects.get(
        wealth=self.wealth,
        id=self.cleaned_data['account_id'])
    amount_to = amount
    if is_conversion_needed(account_from, account_to):
      amount_to = get_converted_amount_transfer(amount, final, rate)
    split_from = AccountSplit(
        date=date,
        wealth=self.wealth,
        amount=amount * -1,
        transaction=transaction,
        type=transaction_type,
        account=account_from)
    split_to = AccountSplit(
        date=date,
        wealth=self.wealth,
        amount=amount_to,
        transaction=transaction,
        type=transaction_type,
        account=account_to)
    split_from.save()
    split_to.save()
    return transaction
 

class TransactionEditForm(MoneypitForm):
  type = ChoiceField(choices=Transaction.TYPES)
  description = CharField(required=False)
  amount = DecimalField(initial=0.0)
  date = DateField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(TransactionEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(
        queryset=Transaction.objects.filter(wealth=self.wealth))

  def clean_amount(self):
    amount = self.cleaned_data['amount']
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount


class TransactionEditNonTransferForm(TransactionEditForm):
  def __init__(self, *args, **kwargs):
    categories_list = kwargs.pop('categories_list', None)
    super(TransactionEditNonTransferForm, self).__init__(*args, **kwargs)

    self.fields['category_id'] = ChoiceField(
        choices=categories_list, required=False)

  def clean_category_id(self):
    try:
      category_id = int(self.cleaned_data['category_id'])
    except ValueError:
      raise ValidationError('Invalid category ID')
    return category_id

  def clean(self):
    super(TransactionEditNonTransferForm, self).clean()
    cleaned_data = self.cleaned_data
    transaction = cleaned_data['id']
    amount = cleaned_data['amount']
    transaction_type = int(cleaned_data['type'])

    account_split = AccountSplit.objects.get(
        wealth=self.wealth,
        transaction=transaction)
    account_from = account_split.account

    if cleaned_data['date'] < account_from.opened_date:
      self.add_error(
          'date',
          'Transaction cannot be made before the account existed')

    return cleaned_data

  def save(self):
    transaction = self.cleaned_data['id']
    date = self.cleaned_data['date']
    description = self.cleaned_data['description']
    transaction_type = int(self.cleaned_data['type'])

    transaction.description = description
    transaction.date = date
    transaction.save()

    amount = self.cleaned_data['amount']
    date = self.cleaned_data['date']
    transaction_type = int(self.cleaned_data['type'])

    account_split = AccountSplit.objects.get(
        wealth=self.wealth,
        transaction=transaction)
    account_split.date = date
    account = account_split.account

    amount_account, amount_category = get_category_amounts(
        account,
        self.wealth,
        amount,
        transaction_type)

    category_split = CategorySplit.objects.get(
        wealth=self.wealth,
        transaction=transaction)
    category_split.date = date
    category = category_split.category

    account_split.amount = amount_account
    category_split.amount = amount_category

    if self.cleaned_data['category_id']:
      new_category = Category.objects.get(
          wealth=self.wealth,
          id=self.cleaned_data['category_id'])
      category_split.category = new_category

    tags = TagSplit.objects.filter(
        wealth=self.wealth,
        transaction=transaction)
    for tag in tags:
      tag.date = date
      tag.amount = account_split.amount
      tag.save()

    account_split.save()
    category_split.save()


class TransactionEditTransferForm(TransactionEditForm):
  def __init__(self, *args, **kwargs):
    accounts_list = kwargs.pop('accounts_list', None)
    super(TransactionEditTransferForm, self).__init__(*args, **kwargs)
    self.fields['account_from'] = ChoiceField(choices=accounts_list)

  def clean_account_id(self):
    account_id = self.cleaned_data['account_id']
    return int(account_id)

  def clean(self):
    super(TransactionEditTransferForm, self).clean()
    cleaned_data = self.cleaned_data
    transaction = cleaned_data['id']
    amount = cleaned_data['amount']
    transaction_type = int(cleaned_data['type'])

    if not cleaned_data['account_from']:
      self.add_error('account_from', 'Account is a compulsory argument')

    account_from = Account.objects.get(
        wealth=self.wealth,
        id=cleaned_data['account_from'])

    if cleaned_data['date'] < account_from.opened_date:
      self.add_error(
          'date',
          'Transaction cannot be made before the account existed')
    split_from = AccountSplit.objects.get(
        wealth=self.wealth,
        transaction=transaction,
        account=account_from)
    try:
      account_split = AccountSplit.objects.get(
          ~Q(account=account_from),
          transaction=transaction,
          wealth=self.wealth)
      account_to = account_split.account
      if cleaned_data['date'] < account_to.opened_date:
        self.add_error(
            'date',
            'Transaction cannot be made before the account existed')
    except ObjectDoesNotExist:
      pass  # destination account no longer exists

    return cleaned_data

  def save(self):
    transaction = self.cleaned_data['id']
    date = self.cleaned_data['date']
    description = self.cleaned_data['description']
    transaction_type = int(self.cleaned_data['type'])

    transaction.description = description
    transaction.date = date
    transaction.save()

    amount = self.cleaned_data['amount']
    date = self.cleaned_data['date']
    account = Account.objects.get(
        wealth=self.wealth,
        id=self.cleaned_data['account_from'])
    split = AccountSplit.objects.get(
        wealth=self.wealth,
        transaction=transaction,
        account=account)
    split.date = date

    if split.amount * amount < 0:
      amount *= -1
    split.amount = amount

    split.save()

    try:
      split_to = AccountSplit.objects.get(
          ~Q(account=account),
          transaction=transaction,
          wealth=self.wealth)
      split_to.date = date
      split_to.save()
    except ObjectDoesNotExist:
      pass  # destination account no longer exists


class AssociateTagForm(MoneypitForm):
  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(AssociateTagForm, self).__init__(*args, **kwargs)
    self.fields['associate'] = BooleanField(initial=False, required=False)
    self.fields['tag'] = ModelChoiceField(
        queryset=Tag.objects.filter(wealth=self.wealth))
    self.fields['transactions'] = ModelMultipleChoiceField(
        queryset=Transaction.objects.filter(wealth=self.wealth))

  def clean_transaction(self):
    transactions = self.cleaned_data['transactions']
    for transaction in transactions:
      if transaction.type == Transaction.TYPE_TRANSFER:
        raise ValidationError('Cannot associate transfers')
    return transactions

  def save(self):
    associate = self.cleaned_data['associate']
    tag = self.cleaned_data['tag']
    transactions = self.cleaned_data['transactions']

    for transaction in transactions:
      try:
        tag_split = TagSplit.objects.get(
            wealth=self.wealth,
            tag=tag,
            transaction=transaction)
        if not associate:
          tag_split.delete()
      except ObjectDoesNotExist:
        if associate:
          account_split = AccountSplit.objects.get(
            wealth=self.wealth,
            transaction=transaction)

          tag_split = TagSplit(
              wealth=self.wealth,
              tag=tag,
              transaction=transaction,
              type=transaction.type,
              amount=account_split.amount,
              date=transaction.date)
          tag_split.save()


class DeAssociateTagsForm(MoneypitForm):
  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(DeAssociateTagsForm, self).__init__(*args, **kwargs)
    self.fields['transactions'] = ModelMultipleChoiceField(
        queryset=Transaction.objects.filter(wealth=self.wealth))

  def clean_transaction(self):
    transactions = self.cleaned_data['transactions']
    for transaction in transactions:
      if transaction.type == Transaction.TYPE_TRANSFER:
        raise ValidationError('Cannot de-associate transfers')
    return transactions

  def save(self):
    transactions = self.cleaned_data['transactions']

    for transaction in transactions:
      try:
        tag_split = TagSplit.objects.get(
            wealth=self.wealth,
            transaction=transaction)
        tag_split.delete()
      except ObjectDoesNotExist:
        pass
