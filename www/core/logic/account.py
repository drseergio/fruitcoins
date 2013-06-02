# -*- coding: utf-8 -*-
from core.models import Account
from core.models import AccountSplit
from core.models import CategorySplit
from core.models import Tag
from core.models import TagSplit
from core.models import Transaction
from logging import getLogger

logger = getLogger('core')


def delete(account):
  wealth = account.wealth
  splits = AccountSplit.objects.filter(account=account)

  for split in splits:
    transaction = split.transaction

    if transaction.type != Transaction.TYPE_TRANSFER:
      category_split = CategorySplit.objects.get(
          wealth=wealth,
          transaction=transaction)
      category_split.delete()

      tag_splits = TagSplit.objects.filter(
          wealth=wealth,
          transaction=transaction)
      for tag_split in tag_splits:
        tag_split.delete()
        
    split.delete()
  account.delete()
