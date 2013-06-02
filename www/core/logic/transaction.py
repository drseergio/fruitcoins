# -*- coding: utf-8 -*-
from core.logic import get_converted_amount
from core.logic import is_conversion_needed
from core.models import AccountSplit
from core.models import CategorySplit
from core.models import Split
from core.models import TagSplit
from core.models import Transaction
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from operator import attrgetter
from logging import getLogger

logger = getLogger('core')


def determine_category(split):
  try:
    if split.type == Transaction.TYPE_TRANSFER:
      try:
        other_split = AccountSplit.objects.get(
          ~Q(id=split.id),
          transaction=split.transaction)
        return (
            other_split.account.id,
            other_split.account.name,
            other_split.account.name)
      except ObjectDoesNotExist:
        return (0, 'Transfer', 'Transfer')
    else:
      other_split = CategorySplit.objects.get(
        transaction=split.transaction)
      return (
          other_split.category.id,
          other_split.category.name,
          other_split.category.full_name)
  except ObjectDoesNotExist:
    return (0, '')


def get_category_amounts(account, wealth, amount, transaction_type):
  amount_category = amount
  if is_conversion_needed(account, wealth):
    amount_category = get_converted_amount(amount, account, wealth)

  if transaction_type == Transaction.TYPE_WITHDRAWAL:
    amount_category = amount_category
    amount_account = amount * -1
  else:
    amount_category = amount_category * -1
    amount_account = amount

  return (amount_account, amount_category)


def get_converted_amount_transfer(amount, final, rate):
  if final:
    return Decimal(final)
  else:
    if not rate:
      rate = 1
    return Decimal(rate) * amount


def get_from_splits(splits):
  transactions = []

  for split in splits:
    transaction = split.transaction
    transaction.split = split
    transaction.category_id, transaction.category, transaction.category_full_name = determine_category(split)

    tag_splits = TagSplit.objects.filter(transaction=transaction)
    transaction.tags = [{'id': tag_split.tag.id} for tag_split in tag_splits]

    transactions.append(transaction)

  return sorted(
    sorted(
        transactions,
        key=attrgetter('split.amount')),
    key=attrgetter('date'), reverse=True)


def delete(transaction):
  bases = [
      AccountSplit.objects,
      CategorySplit.objects,
      TagSplit.objects]

  for base in bases:
    splits = base.filter(transaction=transaction)
    for split in splits:
      split.delete()

  transaction.delete()
