# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from fx import get_rate


def get_list(base, wealth):
  obj_list=[(obj.id, obj.name)
      for obj in base.filter(wealth=wealth)]
  obj_list.append((0, 'None'))
  return obj_list


def is_conversion_needed(account_from, account_to):
  return not account_from.currency == account_to.currency


def get_converted_amount(amount, account, wealth):
  if account.currency != wealth.currency:
    return amount * get_rate(
        account.currency.symbol,
        wealth.currency.symbol)
  return amount


def get_date_period(date):
  period = 'Older'

  if is_future(date):
    period = 'Future'
  elif is_today(date):
    period = 'Today'
  elif is_yesterday(date):
    period = 'Yesterday'
  elif is_last_three_days(date):
    period = 'Last 3 days'
  elif is_later_than_this_monday(date):
    period = 'This week'
  elif is_later_than_last_monday(date):
    period = 'Last week'
  elif is_later_than_first_of_this_month(date):
    period = 'This month'
  elif is_later_than_first_of_last_month(date):
    period = 'Last month'
  elif is_later_than_first_of_this_year(date):
    period = 'This fiscal year'

  return period


def is_future(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta < 0:
    return True
  return False


def is_today(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta == 0:
    return True
  return False


def is_yesterday(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta == 1:
    return True
  return False


def is_last_three_days(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta > 1 and delta <= 3:
    return True
  return False


def is_later_than_this_monday(date):
  monday_spec = datetime.today().strftime('%Y %W 1')
  monday_date = datetime.strptime(monday_spec, '%Y %W %w').date()
  delta = (date - monday_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_last_monday(date):
  lastweek_date = datetime.today() + timedelta(weeks=-1)
  monday_spec = lastweek_date.strftime('%Y %W 1')
  monday_date = datetime.strptime(monday_spec, '%Y %W %w').date()
  delta = (date - monday_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_this_month(date):
  first_spec = datetime.today().strftime('%Y %m 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_last_month(date):
  thismonth_spec = datetime.today().strftime('%Y %m 1')
  thismonth_date = datetime.strptime(thismonth_spec, '%Y %m %d').date()
  lastmonth_date = thismonth_date + timedelta(days=-1)
  first_spec = lastmonth_date.strftime('%Y %m 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_this_year(date):
  first_spec = datetime.today().strftime('%Y 1 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False
