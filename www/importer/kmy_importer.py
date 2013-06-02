# -*- coding: utf-8 -*-
from core.models import *
from datetime import datetime
from decimal import Decimal
from fx import get_rate
from gzip import GzipFile
from logging import getLogger
from re import search
from xml.sax import make_parser
from xml.sax import parseString
from xml.sax.handler import ContentHandler

logger = getLogger('importer.kmy')

KMY_TYPE_REGEX = r'^.*\.kmy$'
KMY_TYPE_ACCOUNT_CHECKING = '1'
KMY_TYPE_ACCOUNT_SAVING = '2'
KMY_TYPE_ACCOUNT_CASH = '3'
KMY_TYPE_ACCOUNT_CREDIT = '4'
KMY_TYPE_ACCOUNT_EQUITY = '9'
SPLIT_AMOUNT_REGEX = r'^(-?\d*)/100$'


class KMYImport(object):
  def __init__(self):
    self.extension = 'kmy'

  def is_supported(self, imported_file):
    return search(KMY_TYPE_REGEX, imported_file.name)

  def process(self, wealth, imported_file, account=None):
    gzip_file = GzipFile(fileobj=imported_file.file)
    decompressed = gzip_file.read()
    parser = make_parser()
    model = {
        'accounts': {},
        'categories': {},
        'currency': [],
        'transactions': [],
        'category_splits': [],
        'account_splits': [],
        'wealth': wealth }
    handler = KMYXmlHandler(model)
    parser.setContentHandler(handler)
    parseString(decompressed, handler)

    accounts = model['accounts']
    categories = self.__build_category_tree(model['categories'])
    transactions = model['transactions']
    account_splits = model['account_splits']
    category_splits = model['category_splits']

    # if main currencies differ, re-calculate
    if model['currency'] != model['wealth'].currency:
      exchange_rate = get_rate(model['currency'], model['wealth'].currency)
      for split in category_splits:
        split.amount *= exchange_rate

    self.accounts = accounts.values()
    self.categories = categories.values()
    self.transactions = [transaction for transaction in transactions if transaction.date]
    self.category_splits = [split for split in category_splits if split.category ]
    self.account_splits = [split for split in account_splits if split.account ]
    self.currency = model['currency']

  def get_preview(self):
    objects_envelope = []
    for account in self.accounts:
      objects_envelope.append({
          'description': str(account),
          'type': 'Account'})

    for split in self.account_splits:
      objects_envelope.append({
          'description': str(split),
          'type': 'Transaction'})

    for category in self.categories:
      objects_envelope.append({
          'description': str(category),
          'type': 'Category'})

    return objects_envelope

  def save(self):
    for account in self.accounts:
      account.save()
    for category in self.categories:
      self._save_category(category)

    category_splits = [split for split in self.category_splits if split.category.id ]

    # set TRANSFER type
    for transaction in self.transactions:
      is_transfer = True
      for split in transaction.splits:
        if isinstance(split, CategorySplit) and split.category.id:
          is_transfer = False
      if is_transfer:
        transaction.type = Transaction.TYPE_TRANSFER
        for split in transaction.splits:
          split.type = transaction.type 

      transaction.save()

    for split in self.account_splits:
      split.account = Account.objects.get(id=split.account.id)
      split.transaction = Transaction.objects.get(id=split.transaction.id)
      split.save()

    for split in category_splits:
      split.category = Category.objects.get(id=split.category.id)
      split.transaction = Transaction.objects.get(id=split.transaction.id)
      split.save()

  def _save_category(self, category):
    if category.parent:
      parent = self._save_category(category.parent)
      category.parent = parent
    category.save()
    return category

  def __build_category_tree(self, categories):
    # fully restore category hierarchy
    for category in categories.values():
      if hasattr(category, 'parentaccount') and categories.get(category.parentaccount):
        category.parent = categories.get(category.parentaccount)
    # set category types
    for category in categories.values():
      root_category = self.__get_category_root(category)
      if hasattr(root_category, 'type'):
        category.type = root_category.type
    # remove any non income/non expense categories
    return dict((category_id,category) for (category_id, category) in categories.items() if category.type)

  def __get_category_root(self, category):
    if category.parent:
      return self.__get_category_root(category.parent)
    else:
      return category


class KMYXmlHandler(ContentHandler):
  """Parses KMYMoney XML data file into a Python model object.

  This class implements SAX interface to parse KMYMoney XML data
  file to create a Python representation which can be later used
  by the import process.

  Attributes:
      model: KMYMoney model object which will hold all parsed info
  """

  def __init__(self, model):
    self.model = model

  def startElement(self, name, attrs):
    if name == 'ADDRESS':
      pass
    elif name == 'ACCOUNT' and not hasattr(self, 'in_budgets'):
      # we're handling an institution account
      if attrs['id'] in self.model['accounts']:
        self.__populate_account(self.model['accounts'][attrs['id']], attrs)
      # ignore opening balance objects
      elif attrs['parentaccount'] == 'AStd::Equity':
        return
      # we're handling a cash account
      elif attrs['parentaccount'] == 'AStd::Asset' or attrs['parentaccount'] == 'AStd::Liability':
        account = self.__create_account(attrs)
        self.__populate_account(account, attrs)
      # we're handling categories
      elif attrs['id'] == 'AStd::Expense':
        self.in_expense_category = True
      elif attrs['id'] == 'AStd::Income':
        self.in_income_category = True
      else:
        self.__create_ordinary_category(attrs)
    elif name == 'TRANSACTION' and hasattr(self, 'in_transactions'):
      self.__create_transaction(attrs)
    elif name == 'SPLIT' and hasattr(self, 'transaction'):
      self.__create_split(attrs)
    elif name == 'SUBACCOUNT':
      self.__create_root_category(attrs)
    elif name == 'BUDGETS':
      self.in_budgets = True
    elif name == 'TRANSACTIONS':
      self.in_transactions = True
    elif name == 'PAIR':
      if attrs['key'] == 'kmm-baseCurrency':
        self.model['currency'] = self.__create_currency(attrs['value'])

  def endElement(self, name):
    if name == 'ACCOUNT' and hasattr(self, 'account'):
      del self.account
    if name == 'ACCOUNT' and hasattr(self, 'in_expense_category'):
      del self.in_expense_category
    if name == 'ACCOUNT' and hasattr(self, 'in_income_category'):
      del self.in_income_category
    if name == 'BUDGETS':
      del self.in_budgets
    if name == 'TRANSACTIONS':
      del self.in_transactions
    if name == 'TRANSACTION' and hasattr(self, 'in_transactions'):
      del self.transaction

  def characters(self, ch):
    return

  def __create_currency(self, symbol):
    return Currency.objects.get(symbol=symbol)

  def __create_account(self, attrs):
    account = AssetAccount()
    account.type = Account.TYPE_ASSET
    self.model['accounts'][attrs['id']] = account
    account.wealth = self.model['wealth']
    return account

  def __populate_account(self, account, attrs):
    account.name = attrs['name']
    account.opened_date = attrs['opened']
    if attrs['lastmodified']:
      account.modified_date = attrs['lastmodified']
    else:
      account.modified_date = datetime.now().strftime('%Y-%m-%d')
    account.currency = self.__create_currency(attrs['currency'])
    old_account = account

    if attrs['type'] == KMY_TYPE_ACCOUNT_SAVING:
      account = SavingsAccount()
      account.type = Account.TYPE_SAVING
      self.model['accounts'][attrs['id']] = account
    elif attrs['type'] == KMY_TYPE_ACCOUNT_CHECKING:
      account = CheckingAccount()
      account.type = Account.TYPE_CHECKING
      self.model['accounts'][attrs['id']] = account
    elif attrs['type'] == KMY_TYPE_ACCOUNT_CASH:
      account = CashAccount()
      account.type = Account.TYPE_CASH
      self.model['accounts'][attrs['id']] = account
    elif attrs['type'] == KMY_TYPE_ACCOUNT_CREDIT:
      account = CreditAccount()
      account.type = Account.TYPE_CREDIT
      self.model['accounts'][attrs['id']] = account
    elif attrs['type'] == KMY_TYPE_ACCOUNT_EQUITY:
      account = AssetAccount()
      account.type = Account.TYPE_ASSET
      self.model['accounts'][attrs['id']] = account
    else:
      del self.model['accounts'][attrs['id']]
      return

    account.name = old_account.name
    account.opened_date = old_account.opened_date
    account.modified_date = old_account.modified_date
    account.currency = old_account.currency
    account.wealth = old_account.wealth

  def __create_split(self, attrs):
    id = attrs['account']
    split = Split()

    amount = Decimal(search(SPLIT_AMOUNT_REGEX, attrs['shares']).group(1)) / 100
    # split for a real account, assing to account
    if self.model['accounts'].has_key(id):
      split = AccountSplit()
      account = self.model['accounts'][id]
      split.account = account
      self.model['account_splits'].append(split)

      if amount < 0:
        split.type = Transaction.TYPE_WITHDRAWAL
      else:
        split.type = Transaction.TYPE_DEPOSIT
    # assign split to category
    elif self.model['categories'].has_key(id):
      split = CategorySplit()
      category = self.model['categories'][id]
      split.category = category
      self.model['category_splits'].append(split)
      if amount < 0:
        split.type = Transaction.TYPE_DEPOSIT
      else:
        split.type = Transaction.TYPE_WITHDRAWAL

    split.amount = amount
    split.transaction = self.transaction
    split.transaction.splits.append(split)
    split.transaction.type = split.type
    split.transaction.description = attrs['memo']
    split.date = split.transaction.date
    split.wealth = self.model['wealth']

  def __create_ordinary_category(self, attrs):
    if attrs['id'] in self.model['categories']:
      self.__populate_category(self.model['categories'][attrs['id']], attrs)
    elif attrs['parentaccount']:
      category = Category()
      self.__populate_category(category, attrs)
      self.model['categories'][attrs['id']] = category

  def __create_root_category(self, attrs):
    if hasattr(self, 'in_expense_category'):
      category = Category()
      category.type = Category.TYPE_EXPENSE
      self.model['categories'][attrs['id']] = category
    elif hasattr(self, 'in_income_category'):
      category = Category()
      category.type = Category.TYPE_INCOME
      self.model['categories'][attrs['id']] = category

  def __populate_category(self, category, attrs):
    category.name = attrs['name']
    category.parentaccount = attrs['parentaccount']
    category.wealth = self.model['wealth']

  def __create_transaction(self, attrs):
    self.transaction = Transaction()
    self.transaction.date = datetime.strptime(attrs['postdate'], '%Y-%m-%d')
    self.transaction.description = attrs['memo']
    self.transaction.wealth = self.model['wealth']
    self.transaction.splits = []
    self.model['transactions'].append(self.transaction)
    self.__create_currency(attrs['commodity'])

