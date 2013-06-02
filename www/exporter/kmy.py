# -*- coding: utf-8 -*-
from core.models import AbstractAccount
from core.models import Account
from core.models import AccountSplit
from core.models import Category
from core.models import CategorySplit
from core.models import Currency
from core.models import Transaction
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
from math import pow
from xml.dom.minidom import getDOMImplementation

KMY_TYPES = [{
        'type': '16',
        'name': 'Equity',
        'class': Account,
        'moneypit_types': [ Account.TYPE_ASSET ]
    }, {
        'type': '9',
        'name': 'Asset',
        'class': Account,
        'moneypit_types': [
            Account.TYPE_SAVING,
            Account.TYPE_CHECKING,
            Account.TYPE_CASH ]
    }, {
        'type': '10',
        'name': 'Liability',
        'class': Account,
        'moneypit_types': [ Account.TYPE_CREDIT ]
    }, {
        'type': '12',
        'name': 'Income',
        'class': Category,
        'moneypit_types': [ Category.TYPE_INCOME ]
    }, {
        'type': '13',
        'name': 'Expense',
        'class': Category,
        'moneypit_types': [ Category.TYPE_EXPENSE ]}]


def export(wealth):
  impl = getDOMImplementation()
  
  dt = impl.createDocumentType('KMYMONEY-FILE', None, None)
  doc = impl.createDocument(None, 'KMYMONEY-FILE', dt)
  root = doc.documentElement
  root.appendChild(_create_info(doc))
  root.appendChild(_create_accounts(doc, wealth))
  root.appendChild(_create_currency(doc, wealth))
  root.appendChild(_create_transactions(doc, wealth))
  root.appendChild(_create_currencies_list(doc))
  return doc.toprettyxml(indent=' ', encoding='utf-8')


def _create_info(doc):
  now = datetime.now()
  fileinfo = doc.createElement('FILEINFO')
  create_date = doc.createElement('CREATION_DATE')
  create_date.setAttribute('date', now.strftime('%Y-%m-%d'))
  modified_date = doc.createElement('LAST_MODIFIED_DATE')
  modified_date.setAttribute('date', now.strftime('%Y-%m-%d'))
  version = doc.createElement('VERSION')
  version.setAttribute('id', '1')
  fixversion = doc.createElement('FIXVERSION')
  fixversion.setAttribute('id', '2')
  fileinfo.appendChild(create_date)
  fileinfo.appendChild(modified_date)
  fileinfo.appendChild(version)
  fileinfo.appendChild(fixversion)
  return fileinfo


def _create_currency(doc, wealth):
  currency = doc.createElement('KEYVALUEPAIRS')
  pair = doc.createElement('PAIR')
  pair.setAttribute('key', 'kmm-baseCurrency')
  pair.setAttribute('value', wealth.currency.symbol)
  currency.appendChild(pair)
  return currency


def _create_accounts(doc, wealth):
  accounts_element = doc.createElement('ACCOUNTS')

  for kmy_map in KMY_TYPES:
    accounts_element.appendChild(_create_toplevel_account(doc, wealth, kmy_map))

  for kmy_map in KMY_TYPES:
    _append_accounts(accounts_element, doc, wealth, kmy_map)
  #_append_accounts(accounts_element, doc, Category, wealth)

  accounts_element.setAttribute('count', str(len(accounts_element.childNodes)))
  return accounts_element


def _append_accounts(accounts_element, doc, wealth, kmy_map):
  account_class = kmy_map['class']
  for account_type in kmy_map['moneypit_types']:
    queryset = account_class.objects.filter(wealth=wealth, type=account_type)
    for item in queryset:
      accounts_element.appendChild(_create_account_item(doc, wealth, item, kmy_map))


def _create_toplevel_account(doc, wealth, kmy_map):
  account_element = doc.createElement('ACCOUNT')
  account_class = kmy_map['class']
  account_element.setAttribute('id', 'AStd::%s' % kmy_map['name'])
  account_element.setAttribute('description', '')
  account_element.setAttribute('parentaccount', '')
  account_element.setAttribute('currency', wealth.currency.symbol)
  account_element.setAttribute('name', kmy_map['name'])
  account_element.setAttribute('opened', '')
  account_element.setAttribute('type', kmy_map['type'])

  all_children = []
  for account_type in kmy_map['moneypit_types']:
    children = account_class.objects.filter(wealth=wealth, parent=None, type=account_type)
    for child in children:
      all_children.append(child)
  return _handle_account_common(doc, account_element, all_children)


def _create_account_item(doc, wealth, item, kmy_map):
  account_element = doc.createElement('ACCOUNT')
  children = item.__class__.objects.filter(wealth=wealth, parent=item)
  account_element.setAttribute('id', _get_account_id(item.id))
  account_element.setAttribute('description', item.description)
  if not item.parent:
    parentaccount = 'AStd::%s' % kmy_map['name']
  else:
    parentaccount = _get_account_id(item.parent.id)
  account_element.setAttribute('parentaccount', parentaccount)
  account_element.setAttribute('name', item.name)
  if hasattr(item, 'currency'):
    currency = item.currency.symbol
  else:
    currency = wealth.currency.symbol
  account_element.setAttribute('currency', currency)
  if hasattr(item, 'opened_date'):
    account_element.setAttribute('opened', item.opened_date.strftime('%Y-%m-%d'))
  else:
    account_element.setAttribute('opened', '')
  account_element.setAttribute('type', kmy_map['type'])
  return _handle_account_common(doc, account_element, children)


def _handle_account_common(doc, account_element, children):
  account_element.setAttribute('institution', '')
  account_element.setAttribute('lastreconciled', '')
  account_element.setAttribute('lastmodified', '')
  account_element.setAttribute('number', '')

  if children:
    subaccounts = doc.createElement('SUBACCOUNTS')
    account_element.appendChild(subaccounts)
    for child in children:
      subaccount = doc.createElement('SUBACCOUNT')
      subaccount.setAttribute('id', _get_account_id(child.id))
      subaccounts.appendChild(subaccount)
  return account_element


def _get_account_id(id):
  return 'A%0*d' % (6, id % 1000000)


def _create_currencies_list(doc):
  currencies_element = doc.createElement('CURRENCIES')
  currencies = Currency.objects.all()

  for currency in currencies:
    currency_element = doc.createElement('CURRENCY')
    if currency.unit == 'N.A.':
      fraction = str(1000000)
    else:
      fraction = str(int(pow(10, int(currency.unit))))
    currency_element.setAttribute('saf', fraction)
    currency_element.setAttribute('ppu', fraction)
    currency_element.setAttribute('scf', fraction)
    currency_element.setAttribute('type', '3')
    currency_element.setAttribute('id', currency.symbol)
    currency_element.setAttribute('symbol', currency.symbol)
    currency_element.setAttribute('name', currency.name)
    currencies_element.appendChild(currency_element)

  currencies_element.setAttribute('count', str(len(currencies)))
  return currencies_element


def _create_transactions(doc, wealth):
  transactions_element = doc.createElement('TRANSACTIONS')
  transactions = Transaction.objects.filter(wealth=wealth).order_by('id')
  for transaction in transactions:
    transactions_element.appendChild(_create_transaction(doc, transaction))

  transactions_element.setAttribute('count', str(len(transactions)))

  return transactions_element


def _create_transaction(doc, transaction):
  transaction_element = doc.createElement('TRANSACTION')
  transaction_element.setAttribute('id', 'T%0*d' % (18, transaction.id % 1000000000000000000))
  transaction_element.setAttribute('postdate', str(transaction.date))
  transaction_element.setAttribute('memo', transaction.description)
  transaction_element.setAttribute('commodity', '')
  transaction_element.setAttribute('entrydate', str(transaction.date))
  splits_element = doc.createElement('SPLITS')
  transaction_element.appendChild(splits_element)

  account_splits = AccountSplit.objects.filter(transaction=transaction)
  i = 0
  for split in account_splits:
    i += 1
    split_element = doc.createElement('SPLIT')
    split_element.setAttribute('id', 'S%0*d' % (4, i))
    split_element.setAttribute('shares', '%d/100' % (split.amount * 100))
    split_element.setAttribute('amount', '%d/100' % (split.amount * 100))
    split_element.setAttribute('account', _get_account_id(split.account.id))
    split_element.setAttribute('reconcileflag', '0')
    split_element.setAttribute('reconciledate', '')
    split_element.setAttribute('action', '')
    split_element.setAttribute('bankid', '')
    split_element.setAttribute('number', '')
    split_element.setAttribute('memo', transaction.description)
    splits_element.appendChild(split_element)

  try:
    split = CategorySplit.objects.get(transaction=transaction)
    i += 1
    split_element = doc.createElement('SPLIT')
    split_element.setAttribute('id', 'S%0*d' % (4, i))
    split_element.setAttribute('shares', '%d/100' % (split.amount * 100))
    split_element.setAttribute('account', _get_account_id(split.category.id))
    split_element.setAttribute('amount', '%d/100' % (split.amount * 100))
    split_element.setAttribute('reconcileflag', '0')
    split_element.setAttribute('reconciledate', '')
    split_element.setAttribute('action', '')
    split_element.setAttribute('bankid', '')
    split_element.setAttribute('number', '')
    split_element.setAttribute('memo', transaction.description)
    splits_element.appendChild(split_element)
  except ObjectDoesNotExist:
    pass

  return transaction_element
