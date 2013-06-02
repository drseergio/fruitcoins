# -*- coding: utf-8 -*-
from core.models import Account
from core.models import AccountSplit
from core.models import Category
from core.models import CategorySplit
from core.models import Transaction
from csv import reader
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from fx import get_rate
from logging import getLogger
from re import search

logger = getLogger('importer.csv')

TYPE_REGEX = r'^.*\.csv$'


class CSVImport(object):
  def __init__(self):
    self.extension = 'csv'

  def is_supported(self, imported_file):
    return search(TYPE_REGEX, imported_file.name)

  def process(self, wealth, imported_file, account):
    csv_file = imported_file.file
    rows = reader(csv_file)

    self.categories = [];
    self.transactions = [];
    self.category_splits = [];
    self.account_splits = [];
    self.wealth = wealth;

    for row in rows:
      self._process_row(row, account)

  def save(self):
    for category in self.categories:
      category.save()
    for transaction in self.transactions:
      transaction.save()
    for split in self.account_splits:
      split.transaction = Transaction.objects.get(id=split.transaction.id)
      split.save()
    for split in self.category_splits:
      split.transaction = Transaction.objects.get(id=split.transaction.id)
      split.category = Category.objects.get(id=split.category.id)
      split.save()

  def _process_row(self, row, from_account):
    date = datetime.strptime(row[1], '%Y-%m-%d')
    description = row[2]
    category = row[3]
    amount = Decimal(row[4])

    try:
      to_account = Account.objects.get(
          wealth=self.wealth,
          name=category)
      self._create_transfer(
          from_account,
          to_account,
          date,
          description,
          amount)
    except ObjectDoesNotExist:
      if amount < 0:
        category_type = Category.TYPE_EXPENSE
        transaction_type = Transaction.TYPE_WITHDRAWAL
      else:
        category_type = Category.TYPE_INCOME
        transaction_type = Transaction.TYPE_DEPOSIT

      try:
        category = Category.objects.get(
            wealth=self.wealth,
            full_name=category,
            type=category_type)
      except ObjectDoesNotExist:
        category = self._create_category(category, category_type)
      self._create_nontransfer(
          from_account,
          category,
          date,
          description,
          amount,
          transaction_type)

  def _create_transfer(self, from_account, to_account, date, description, amount):
    if from_account == to_account:
      return
    transaction = Transaction(
        type=Transaction.TYPE_TRANSFER,
        date=date,
        description=description,
        wealth=self.wealth)
    self.transactions.append(transaction)
    account_split = AccountSplit(
        account=from_account,
        amount=amount,
        date=date,
        transaction=transaction,
        type=Transaction.TYPE_TRANSFER,
        wealth=self.wealth)
    self.account_splits.append(account_split)
    account_split = AccountSplit(
        account=to_account,
        amount=amount * -1,
        date=date,
        transaction=transaction,
        type=Transaction.TYPE_TRANSFER,
        wealth=self.wealth)
    self.account_splits.append(account_split)

  def _create_nontransfer(self, from_account, category, date, description, amount,
      transaction_type):
    transaction = Transaction(
        type=transaction_type,
        date=date,
        description=description,
        wealth=self.wealth)
    self.transactions.append(transaction)
    account_split = AccountSplit(
        account=from_account,
        amount=amount,
        date=date,
        transaction=transaction,
        type=transaction_type,
        wealth=self.wealth)
    self.account_splits.append(account_split)
    category_split = CategorySplit(
        category=category,
        date=date,
        amount=amount * -1,
        transaction=transaction,
        type=transaction_type,
        wealth=self.wealth)
    self.category_splits.append(category_split)

  def _create_category(self, name, category_type):
    hierarchy = name.split(':')
    accumulated = []
    parent = None
    for level in hierarchy:
      accumulated.append(level)
      try:
        category = Category.objects.get(
            wealth=self.wealth,
            type=category_type,
            full_name=':'.join(accumulated))
      except ObjectDoesNotExist:
        category = Category(
            wealth=self.wealth,
            name=level,
            balance=0,
            type=category_type,
            parent=parent)
        self.categories.append(category)
      parent = category
    return parent
