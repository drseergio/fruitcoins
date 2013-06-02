# -*- coding: utf-8 -*-
from api import load_params
from core.forms.budget import BudgetAddForm
from core.logic.budget import delete_budget
from core.models import Budget
from django.db import transaction
from django.utils import simplejson
from piston.handler import BaseHandler
from piston.utils import rc


class BudgetHandler(BaseHandler):
  model = Budget

  def read(self, request, budget_id=None):
    wealth = request.session['wealth']
    base = Budget.objects

    if budget_id:
      return self._handle_get(base.get(
          wealth=wealth,
          id=budget_id))
    else:
      budgets = base.filter(wealth=wealth).order_by('-year')
      return self._handle_index(budgets)

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = load_params(request)

    form = BudgetAddForm(params, wealth=wealth)
    if form.is_valid():
      budget = form.save()
      return {'success': True, 'id': budget.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, budget_id):
    wealth = request.session['wealth']

    budget = Budget.objects.get(
        wealth=wealth,
        id=budget_id)
    delete_budget(budget)
    return {'success': True}

  def _handle_index(self, budgets):
    budgets_return = []
    for budget in budgets:
      budgets_return.append({
          'id': budget.id,
          'name': budget.name,
          'year': str(budget.year)})
    return budgets_return

  def _handle_get(self, budget):
    return {
        'name': budget.name,
        'id': budget.id,
        'year': str(budget.year)}
