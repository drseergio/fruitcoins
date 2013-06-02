# -*- coding: utf-8 -*-
from core.models import Account
from core.models import Category
from core.models import Transaction
from logging import getLogger

logger = getLogger('core')


def save_models(import_data):
  accounts = import_data['accounts']
  categories = import_data['categories']
  transactions = import_data['transactions']
  account_splits = import_data['account_splits']
  category_splits = import_data['category_splits']

  for account in accounts:
    account.save()
  for category in categories:
    _save_category(category)

  for transaction in transactions:
    transaction.save()

  for split in account_splits:
    split.account = Account.objects.get(id=split.account.id)
    split.transaction = Transaction.objects.get(id=split.transaction.id)
    split.save()

  try:
    for split in category_splits:
      split.category = Category.objects.get(id=split.category.id)
      split.transaction = Transaction.objects.get(id=split.transaction.id)
      split.save()
  except Exception, e:
    logger.exception(e)


def _save_category(category):
  if category.parent:
    parent = _save_category(category.parent)
    category.parent = parent
  category.save()
  return category
