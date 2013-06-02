# -*- coding: utf-8 -*-
from core.models import AccountSplit
from datetime import datetime
from django.db import connection
from django.db import transaction
from fx import get_rate
from logging import getLogger
from math import fabs

logger = getLogger('core')

SQL_NETWORTH_MONTH = "SELECT SUM(local_amount) FROM core_accountsplit WHERE wealth_id = %d AND date < '%s'"
SQL_EXPENSES_MONTH = "SELECT SUM(amount) FROM core_categorysplit WHERE wealth_id = %d AND type = %d AND YEAR(date) = %d AND MONTH(date) = %d"
SQL_CATEGORY_BD = "SELECT core_category.full_name, SUM(amount) FROM core_categorysplit INNER JOIN core_category ON core_category.abstractaccount_ptr_id = core_categorysplit.category_id WHERE wealth_id = %d AND core_categorysplit.type = %d AND date > '%s' AND date < '%s' GROUP BY core_category.abstractaccount_ptr_id"


def get_networth(wealth, date_from, date_to):
  dates = _calculate_dates(date_from, date_to)
  obj_envelope = []

  cursor = connection.cursor()
  for date in dates:
    cursor.execute(SQL_NETWORTH_MONTH % (wealth.id, date.strftime('%Y/%m/%d')))
    row = cursor.fetchone()
    obj_envelope.append({ 'month': date.strftime('%b %Y'), 'balance': row[0] })
  return obj_envelope


def get_expenses(wealth, date_from, date_to):
  dates = _calculate_dates(date_from, date_to)
  obj_envelope = []

  cursor = connection.cursor()
  for date in dates:
    cursor.execute(SQL_EXPENSES_MONTH % (wealth.id, 1, date.year, date.month))
    row = cursor.fetchone()
    obj_envelope.append({ 'month': date.strftime('%b %Y'), 'amount': row[0] })
  return obj_envelope


def get_incomes(wealth, date_from, date_to):
  dates = _calculate_dates(date_from, date_to)
  obj_envelope = []

  cursor = connection.cursor()
  for date in dates:
    cursor.execute(SQL_EXPENSES_MONTH % (wealth.id, 2, date.year, date.month))
    row = cursor.fetchone()
    obj_envelope.append({ 'month': date.strftime('%b %Y'), 'amount': fabs(row[0]) })
  return obj_envelope


def get_category_breakdown(wealth, split_type, date_from, date_to):
  obj_envelope = []
  cursor = connection.cursor()
  cursor.execute(SQL_CATEGORY_BD % (
      wealth.id,
      split_type,
      date_from.strftime('%Y/%m/%d'),
      date_to.strftime('%Y/%m/%d')))
  rows = cursor.fetchall()
  for row in rows:
    full_name = row[0]
    short_name = full_name.split(':')[-1]
    obj_envelope.append({
        'name': short_name,
        'full_name': full_name,
        'amount': fabs(row[1]) })
  return obj_envelope


def _calculate_dates(date_from, date_to):
  start_month = date_from.month
  end_months = (date_to.year - date_from.year) * 12 + date_to.month + 1
  return [datetime(year=yr, month=mn, day=1) for (yr, mn) in (
      ((m - 1) / 12 + date_from.year, (m - 1) % 12 + 1) for m in range(start_month, end_months))]
