# -*- coding: utf-8 -*-
from core.logic.transaction import get_from_splits
from csv import writer
from datetime import datetime
from django.http import HttpResponse


def export(wealth, splits, view_type, name):
  transactions = get_from_splits(splits)

  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = ('attachment; filename=moneypit-'
      '%s-%s-%s.csv') % (
          view_type,
          name.replace(' ', '-'),
          datetime.now().strftime('%Y%m%d'))
  csv_writer = writer(response)

  i = 0
  for transaction in transactions:
    csv_writer.writerow([
        i,
        str(transaction.date),
        transaction.description,
        str(transaction.category_full_name),
        str(transaction.split.amount)])
    i += 1

  return response
