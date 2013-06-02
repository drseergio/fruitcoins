# -*- coding: utf-8 -*-
from api import load_params
from api.decorators import require_args
from core.forms.budgetline import BudgetLineAddForm
from core.forms.budgetline import BudgetLineEditForm
from core.models import Budget
from core.models import BudgetLine
from core.models import Category
from decimal import Decimal
from django.db import transaction
from django.utils import simplejson
from logging import getLogger
from math import fabs
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api')


class BudgetLineHandler(BaseHandler):
  model = BudgetLine

  @require_args(['budget'], 'GET')
  def read(self, request, budgetline_id=None):
    wealth = request.session['wealth']
    base = BudgetLine.objects
    if budgetline_id:
      return self._handle_get(base.get(
          wealth=wealth,
          id=budgetline_id))
    else:
      budget = Budget.objects.get(wealth=wealth, id=request.GET['budget'])
      return self._handle_index(base.filter(
          wealth=wealth, budget=budget).order_by('type'))

  @transaction.commit_on_success
  @require_args(['budget'], 'GET')
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = load_params(request)
    params['budget'] = request.GET['budget']

    form = BudgetLineAddForm(
        params,
        wealth=wealth)
    if form.is_valid():
      budgetline = form.save()
      return {'success': True, 'id': budgetline.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  @require_args(['budget'], 'GET')
  def update(self, request, budgetline_id):
    wealth = request.session['wealth']
    params = load_params(request)
    params['budget'] = request.GET['budget']
    params['id'] = budgetline_id

    budgetline = BudgetLine.objects.get(
        wealth=wealth,
        id=budgetline_id)

    form = BudgetLineEditForm(
        params,
        wealth=wealth)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  @require_args(['budget'], 'GET')
  def delete(self, request, budgetline_id):
    wealth = request.session['wealth']
    budget_id = request.GET['budget']
    budget = Budget.objects.get(
        wealth=wealth,
        id=budget_id)

    budgetline = BudgetLine.objects.get(
        wealth=wealth,
        budget=budget,
        id=budgetline_id)

    budgetline.delete()
    return {'success': True}

  def _handle_get(self, budgetline):
    return {
        'type': budgetline.type,
        'category': budgetline.category.name,
        'category_id': budgetline.category.id,
        'amount': str(budgetline.amount),
        'total_amount': str(budgetline.total_amount),
        'period': budgetline.period,
        'balance': str(budgetline.balance),
        'id': budgetline.id }

  def _handle_index(self, budgetlines):
    lines_return = []
    for budgetline in budgetlines:
      lines_return.append({
          'type': budgetline.type,
          'category': budgetline.category.name,
          'category_id': budgetline.category.id,
          'amount': str(budgetline.amount),
          'progress': self._get_progress(
              budgetline.type,
              budgetline.total_amount,
              budgetline.balance),
          'total_amount': str(budgetline.total_amount),
          'period': budgetline.period,
          'balance': str(budgetline.balance),
          'id': budgetline.id })
    return lines_return

  def _get_progress(self, category_type, total_amount, balance):
    if category_type == Category.TYPE_INCOME and balance > 0:
      return 0
    elif category_type == Category.TYPE_EXPENSE and balance < 0:
      return 0
    else:
      return int((fabs(Decimal(balance) / Decimal(total_amount)) * 100))
