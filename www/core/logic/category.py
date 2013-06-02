# -*- coding: utf-8 -*-
from core.models import AccountSplit
from core.models import Category
from core.models import CategorySplit
from django.core.exceptions import ObjectDoesNotExist


def delete(category):
  splits = CategorySplit.objects.filter(category=category)
  for split in splits:
    transaction = split.transaction
    try:
      account_split = AccountSplit.objects.get(
          transaction=transaction)
      account_split.delete()
    except ObjectDoesNotExist:
      pass
    split.delete()
    transaction.delete()
  category.delete()


def change_type(category, new_type):
  children = Category.objects.filter(parent=category)
  category.type = new_type
  category.save()

  if not children:
    return
  else:
    for child in children:
      change_type(child, new_type)
