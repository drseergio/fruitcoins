# -*- coding: utf-8 -*-
from api import JSON_FAILURE
from api import get_json_response
from api.decorators import require_auth
from api.decorators import require_args
from core.logic.report import get_category_breakdown
from core.logic.report import get_expenses
from core.logic.report import get_incomes
from core.logic.report import get_networth
from core.models import Transaction
from datetime import datetime
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.http import require_POST
from piston.utils import rc


@require_auth
@require_args(['date_from', 'date_to'], 'GET', False)
def networth(request):
  wealth = request.session['wealth']
  try:
    date_from, date_to = _validate_dates(request)
  except ValueError:
    return rc.BAD_REQUEST
  report_values = get_networth(wealth, date_from, date_to)
  return get_json_response(report_values, total=len(report_values))


@require_auth
@require_args(['date_from', 'date_to'], 'GET', False)
def expenses(request):
  wealth = request.session['wealth']
  try:
    date_from, date_to = _validate_dates(request)
  except ValueError:
    return rc.BAD_REQUEST
  report_values = get_expenses(wealth, date_from, date_to)
  return get_json_response(report_values, total=len(report_values))


@require_auth
@require_args(['date_from', 'date_to'], 'GET', False)
def incomes(request):
  wealth = request.session['wealth']
  try:
    date_from, date_to = _validate_dates(request)
  except ValueError:
    return rc.BAD_REQUEST
  report_values = get_incomes(wealth, date_from, date_to)
  return get_json_response(report_values, total=len(report_values))


@require_auth
@require_args(['date_from', 'date_to'], 'GET', False)
def netincome(request):
  wealth = request.session['wealth']
  try:
    date_from, date_to = _validate_dates(request)
  except ValueError:
    return rc.BAD_REQUEST
  expenses = get_expenses(wealth, date_from, date_to)
  incomes = get_incomes(wealth, date_from, date_to)

  report_values = []
  for i in range(len(incomes)):
    report_values.append({
        'month': incomes[i]['month'],
        'amount': round(incomes[i]['amount'] - float(expenses[i]['amount']), 2)})
  return get_json_response(report_values, total=len(report_values))


@require_auth
@require_args(['date_from', 'date_to'], 'GET', False)
def categories(request, category_type):
  wealth = request.session['wealth']
  try:
    date_from, date_to = _validate_dates(request, True)
  except ValueError:
    return rc.BAD_REQUEST
  if category_type == 'income':
    split_type = Transaction.TYPE_DEPOSIT
  else:
    split_type = Transaction.TYPE_WITHDRAWAL
  report_values = get_category_breakdown(
      wealth, split_type, date_from, date_to)
  return get_json_response(report_values, total=len(report_values))


def _validate_dates(request, is_same_allowed=False):
  date_from = datetime.strptime(request.GET['date_from'], '%Y-%m-%d')
  date_to = datetime.strptime(request.GET['date_to'], '%Y-%m-%d')

  if date_from > date_to:
    return HttpResponse(JSON_FAILURE % 'From date cannot be in future')

  if date_from.month == date_to.month and date_from.year == date_to.year and not is_same_allowed:
    return HttpResponse(JSON_FAILURE % 'Cannot report on a single month')

  return date_from, date_to
