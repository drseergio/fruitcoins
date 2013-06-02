# -*- coding: utf-8 -*-
from core.logic import get_converted_amount
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from fx.models import Currency
from logging import getLogger
from settings import RECEIPT_STORAGE

logger = getLogger('core')


class InviteRequest(models.Model):
  email = models.CharField(max_length=255)
  date = models.DateField()


class Wealth(models.Model):
  currency = models.ForeignKey(Currency)
  balance = models.DecimalField(decimal_places=2, max_digits=30)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return unicode(self.user)


class WealthTask(models.Model):
  wealth = models.ForeignKey(Wealth)
  name = models.CharField(max_length=255)


class Feedback(models.Model):
  text = models.TextField()
  date = models.DateField()
  wealth = models.ForeignKey(Wealth)


class Receipt(models.Model):
  image = models.ImageField(upload_to=RECEIPT_STORAGE)
  date = models.DateField()
  wealth = models.ForeignKey(Wealth)
  latitude = models.FloatField(blank=True, default=0)
  longitude = models.FloatField(blank=True, default=0)


class AbstractAccount(models.Model):
  name = models.CharField(max_length=255)
  balance = models.DecimalField(decimal_places=2, max_digits=30, default=0)
  wealth = models.ForeignKey(Wealth)
  description = models.TextField(blank=True)
  is_visible = models.BooleanField(default=True)

  def add_balance(self, amount):
    self.balance += amount
    self.save()

  def del_balance(self, amount):
    self.balance -= amount
    self.save()

  def change_balance(self, old_amount, new_amount):
    self.balance -= old_amount
    self.balance += new_amount
    self.save()

  def __unicode__(self):
    return self.name


class Account(AbstractAccount):
  TYPE_SAVING = 1
  TYPE_CHECKING = 2
  TYPE_CASH = 3
  TYPE_CREDIT = 4
  TYPE_BROKER = 5
  TYPE_ASSET = 6

  TYPES = (
      (TYPE_SAVING, 'Saving'),
      (TYPE_CHECKING, 'Checking'),
      (TYPE_CASH, 'Cash'),
      (TYPE_CREDIT, 'Credit Card'),
      (TYPE_BROKER, 'Brokerage'))

  type = models.IntegerField(max_length=2, choices=TYPES)
  parent = models.ForeignKey('self', null=True, blank=True)
  opening_balance = models.DecimalField(decimal_places=2, max_digits=30, default=0)
  total_deposits = models.DecimalField(decimal_places=2, max_digits=30, default=0)
  total_withdrawals = models.DecimalField(decimal_places=2, max_digits=30, default=0)
  opened_date = models.DateField()
  modified_date = models.DateField()
  currency = models.ForeignKey(Currency)

  def add_balance(self, amount, transaction_type):
    if transaction_type == Transaction.TYPE_DEPOSIT:
      self.total_deposits += amount
    elif transaction_type == Transaction.TYPE_WITHDRAWAL:
      self.total_withdrawals += amount
    self.balance += amount
    self.save()

  def del_balance(self, amount, transaction_type):
    if transaction_type == Transaction.TYPE_DEPOSIT:
      self.total_deposits -= amount
    elif transaction_type == Transaction.TYPE_WITHDRAWAL:
      self.total_withdrawals -= amount
    self.balance -= amount
    self.save()

  def change_balance(self, old_amount, new_amount, transaction_type):
    if transaction_type == Transaction.TYPE_DEPOSIT:
      self.total_deposits -= old_amount
      self.total_deposits += new_amount
    elif transaction_type == Transaction.TYPE_WITHDRAWAL:
      self.total_withdrawals -= old_amount
      self.total_withdrawals += new_amount
    self.balance -= old_amount
    self.balance += new_amount
    self.save()

  def calculate_balance(self):
    splits = AccountSplit.objects.filter(
      account=self)
    balance = 0
    total_deposits = 0
    total_withdrawals = 0

    for split in splits:
      balance += split.amount
      if split.type == Transaction.TYPE_DEPOSIT:
        total_deposits += amount
      elif split.type == Transaction.TYPE_WITHDRAWAL:
        total_withdrawals += amount

    self.balance = balance
    self.total_deposits = total_deposits
    self.total_withdrawals = total_withdrawals  
    self.save()

  def __unicode__(self):
    return '%s, (%s)' % (self.name, self.currency.symbol)


class CheckingAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_CHECKING
    super(CheckingAccount, self).__init__(*args, **kwargs)

  def __unicode__(self):
    return '%s %s' % (super(CheckingAccount, self).__unicode__(), 'Checking')


class SavingsAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_SAVING
    super(SavingsAccount, self).__init__(*args, **kwargs)


class BrokerAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_BROKER
    super(BrokerAccount, self).__init__(*args, **kwargs)


class CreditAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_CREDIT
    super(CreditAccount, self).__init__(*args, **kwargs)


class CashAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_CASH
    super(CashAccount, self).__init__(*args, **kwargs)


class AssetAccount(Account):
  def __init__(self, *args, **kwargs):
    self.type = Account.TYPE_ASSET
    super(AssetAccount, self).__init__(*args, **kwargs)


class Category(AbstractAccount):
  TYPE_INCOME = 1
  TYPE_EXPENSE = 2

  TYPES = (
      (TYPE_INCOME, 'Income'),
      (TYPE_EXPENSE, 'Expense'))

  full_name = models.CharField(max_length=1024)
  parent = models.ForeignKey('self', null=True, blank=True)
  total_balance = models.DecimalField(decimal_places=2,
      max_digits=30,
      default=0)
  type = models.IntegerField(max_length=2, choices=TYPES)

  def save(self):
    self.full_name = self.update_full_name(self)
    super(Category, self).save()
    if self.parent:
      self.parent.calculate_total_balance()

  def delete(self):
    parent = self.parent
    super(Category, self).delete()
    if parent:
      parent.calculate_total_balance()

  def update_full_name(self, category):
    if category.parent:
      return '%s:%s' % (self.update_full_name(category.parent), category.name)
    else:
      return category.name

  def calculate_total_balance(self):
    new_balance = 0
    child_categories = Category.objects.filter(parent=self)
    for category in child_categories:
      new_balance += (category.total_balance + category.balance)
    self.total_balance = new_balance
    self.save()

  def __unicode__(self):
    return self.name


class Transaction(models.Model):
  TYPE_WITHDRAWAL = 1
  TYPE_DEPOSIT = 2
  TYPE_TRANSFER = 3

  TYPES = (
      (TYPE_WITHDRAWAL, 'Withdrawal'),
      (TYPE_DEPOSIT, 'Deposit'),
      (TYPE_TRANSFER, 'Transfer'))

  date = models.DateField()
  description = models.TextField(blank=True)
  wealth = models.ForeignKey(Wealth)
  latitude = models.FloatField(blank=True, default=0)
  longitude = models.FloatField(blank=True, default=0)

  type = models.IntegerField(
      max_length=2,
      choices=TYPES,
      default=TYPE_WITHDRAWAL)

  def __unicode__(self):
    return unicode(self.date)


class Tag(AbstractAccount):
  created_date = models.DateField()
  modified_date = models.DateField()


class Split(models.Model):
  date = models.DateField()
  wealth = models.ForeignKey(Wealth)
  amount = models.DecimalField(decimal_places=2, max_digits=30)
  transaction = models.ForeignKey(Transaction)
  latitude = models.FloatField(blank=True, default=0)
  longitude = models.FloatField(blank=True, default=0)

  type = models.IntegerField(
      max_length=2,
      choices=Transaction.TYPES,
      default=Transaction.TYPE_WITHDRAWAL)

  class Meta(object):
    abstract = True


class CategorySplit(Split):
  category = models.ForeignKey(Category)

  def delete(self):
    self.category.del_balance(self.amount)
    try:
      budget_line = BudgetLine.objects.get(
          wealth=self.wealth,
          year=self.date.year,
          category=self.category)
      budget_line.del_balance(self.amount)
    except ObjectDoesNotExist:
      pass
    super(CategorySplit, self).save()

  def save(self):
    if not self.id:
      self.category.add_balance(self.amount)

      try:
        budget_line = BudgetLine.objects.get(
            wealth=self.wealth,
            year=self.date.year,
            category=self.category)
        budget_line.add_balance(self.amount)
      except ObjectDoesNotExist:
        pass
    else:
      old_self = CategorySplit.objects.get(id=self.id)
      if old_self.category != self.category:
        old_self.category.del_balance(old_self.amount)
        self.category.add_balance(self.amount)

        try:
          old_budget_line = BudgetLine.objects.get(
              wealth=self.wealth,
              year=old_self.date.year,
              category=old_self.category)
          old_budget_line.del_balance(old_self.amount)
        except ObjectDoesNotExist:
          pass

        try:
          new_budget_line = BudgetLine.objects.get(
              wealth=self.wealth,
              year=self.date.year,
              category=self.category)
          new_budget_line.add_balance(self.amount)
        except ObjectDoesNotExist:
          pass
      else:
        try:
          budget_line = BudgetLine.objects.get(
              wealth=self.wealth,
              year=self.date.year,
              category=self.category)
          budget_line.change_balance(old_self.amount, self.amount)
        except ObjectDoesNotExist:
          pass
        self.category.change_balance(old_self.amount, self.amount)
    super(CategorySplit, self).save()

  def __unicode__(self):
    transaction_type = Transaction.TYPES[self.type - 1][1]
    return '%.2f on %s, %s %s %s' % (
        self.amount,
        self.date,
        transaction_type,
        self.transaction.description,
        self.category.name)


class AccountSplit(Split):
  account = models.ForeignKey(Account)
  local_amount = models.DecimalField(decimal_places=2, max_digits=30)

  def delete(self):
    self.account.del_balance(self.amount, self.type)
    super(AccountSplit, self).delete()

  def save(self):
    if not self.id:
      self.account.add_balance(self.amount, self.type)
    else:
      old_self = AccountSplit.objects.get(id=self.id)
      self.account.change_balance(old_self.amount, self.amount, self.type)
    if self.account.currency != self.wealth.currency:
      self.local_amount = get_converted_amount(self.amount, self.account, self.wealth)
    else:
      self.local_amount = self.amount
    super(AccountSplit, self).save()

  def __unicode__(self):
    transaction_type = Transaction.TYPES[self.type - 1][1]
    return '%.2f on %s, %s %s [%s]' % (
        self.amount,
        self.date,
        transaction_type,
        self.transaction.description,
        self.account.name)


class TagSplit(Split):
  tag = models.ForeignKey(Tag)

  def delete(self):
    self.tag.modified_date = datetime.utcnow()
    self.tag.del_balance(self.amount)
    super(TagSplit, self).delete()

  def save(self):
    self.tag.modified_date = datetime.utcnow()
    if not self.id:
      self.tag.add_balance(self.amount)
    else:
      old_self = TagSplit.objects.get(id=self.id)
      self.tag.change_balance(old_self.amount, self.amount)
    super(TagSplit, self).save()


class Budget(models.Model):
  wealth = models.ForeignKey(Wealth)
  name = models.CharField(max_length=255)
  year = models.IntegerField()


class BudgetLine(models.Model):
  PERIOD_WEEKLY = 1
  PERIOD_MONTHLY = 2
  PERIOD_QUARTERLY = 3
  PERIOD_YEARLY = 4

  PERIODS = (
      (PERIOD_WEEKLY, 'Weekly'),
      (PERIOD_MONTHLY, 'Monthly'),
      (PERIOD_QUARTERLY, 'Quarterly'),
      (PERIOD_YEARLY, 'Yearly'))

  category = models.ForeignKey(Category)
  amount = models.DecimalField(decimal_places=2, max_digits=30)
  total_amount = models.DecimalField(decimal_places=2, max_digits=30)
  type = models.IntegerField(max_length=2, choices=Category.TYPES) 
  period = models.IntegerField(max_length=2, choices=PERIODS)
  balance = models.DecimalField(decimal_places=2, max_digits=30)
  budget = models.ForeignKey(Budget)
  wealth = models.ForeignKey(Wealth)
  year = models.IntegerField()

  def add_balance(self, amount):
    self.balance += amount
    self.save()

  def del_balance(self, amount):
    self.balance -= amount
    self.save()

  def change_balance(self, old_amount, new_amount):
    self.balance -= old_amount
    self.balance += new_amount
    self.save()

  def save(self):
    if not self.id:
      splits = CategorySplit.objects.filter(
          wealth=self.wealth,
          category=self.category,
          date__year=self.budget.year)
      balance = 0
      for split in splits:
        balance += split.amount
      self.balance = balance

    if self.period == self.PERIOD_WEEKLY:
      self.total_amount = self.amount * 52
    elif self.period == self.PERIOD_MONTHLY:
      self.total_amount = self.amount * 12
    elif self.period == self.PERIOD_QUARTERLY:
      self.total_amount = self.amount * 4
    else:
      self.total_amount = self.amount
    super(BudgetLine, self).save()
