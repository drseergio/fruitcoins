# -*- coding: utf-8 -*-
from api import load_params
from api.decorators import require_auth
from api import get_json_errors
from api import JSON_FAILURE
from api import JSON_SUCCESS
from core.forms.category import CategoryAddForm
from core.forms.category import CategoryEditForm
from core.forms.category import CategoryMoveForm
from core.logic.category import delete as delete_category
from core.models import Category
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.http import require_POST
from piston.handler import BaseHandler
from piston.utils import rc


class CategoryHandler(BaseHandler):
  model = Category

  def read(self, request, category_id=None, search=None):
    wealth = request.session['wealth']
    base = Category.objects

    if category_id:
      category = Category.objects.get(
          wealth=wealth,
          id=category_id)
      return {
          'id': category.id,
          'balance': str(category.balance),
          'text': category.name,
          'description': category.description,
          'total_balance': str(category.balance + category.total_balance)}
    elif 'query' in request.GET and search:
      return self._handle_search(base.filter(
          wealth=wealth,
          full_name__icontains=request.GET['query']))
    else:
      if 'node' not in request.GET:
        return self._handle_search(base.filter(
            wealth=wealth))
      return self._tree(request.GET['node'], wealth)

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = load_params(request)

    form = CategoryAddForm(params, wealth=wealth)
    if form.is_valid():
      category = form.save()
      return {'success': True, 'id': category.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def update(self, request, category_id):
    wealth = request.session['wealth']
    params = load_params(request)
    params['id'] = category_id

    category = Category.objects.get(
        wealth=wealth,
        id=category_id)

    form = CategoryEditForm(
        params,
        wealth=wealth)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, category_id):
    wealth = request.session['wealth']

    category = Category.objects.get(
        wealth=wealth,
        id=category_id)
    delete_category(category)
    return {'success': True}

  def _tree(self, node, wealth):
    if node == '0' or node == 'root':
      expense_categories = self._get_categories(wealth, Category.TYPE_EXPENSE)
      income_categories = self._get_categories(wealth, Category.TYPE_INCOME)

      return [{
          'expanded': True,
          'id': 'exp',
          'text': 'Expense',
          'leaf': False,
          'description': 'Expense categories',
          'balance': '-',
          'total_balance': '-',
          'iconCls': 'expense-icon',
          'children': expense_categories
        }, {
          'expanded': True,
          'id': 'inc',
          'text': 'Income',
          'leaf': False,
          'description': 'Income categories',
          'balance': '-',
          'total_balance': '-',
          'iconCls': 'income-icon',
          'children': income_categories}]
    elif node == 'exp':
      categories = Category.objects.filter(
          wealth=wealth,
          type=Category.TYPE_EXPENSE,
          parent__isnull=True).order_by('name')
      return self._handle_tree(categories)
    elif node == 'inc':
      categories = Category.objects.filter(
          wealth=wealth,
          type=Category.TYPE_INCOME,
          parent__isnull=True).order_by('name')
      return self._handle_tree(categories)
    else:
      Category.objects.get(wealth=wealth, id=node)
      return self._get_categories(wealth, node=node)

  def _get_categories(self, wealth, category_type=None, node=None):
    if not node:
      return [self._handle_category(wealth, category) for category in Category.objects.filter(
          wealth=wealth,
          parent__isnull=True,
          type=category_type)]
    if node:
      return [self._handle_category(wealth, category) for category in Category.objects.filter(
          wealth=wealth,
          parent=node)]

  def _handle_category(self, wealth, category):
    children = self._get_categories(wealth, node=category)

    if category.type == Category.TYPE_EXPENSE:
      icon = 'expense-icon'
    else:
      icon = 'income-icon'

    return {
        'id': category.id,
        'text': category.name,
        'leaf': False,
        'expanded': True,
        'description': category.description,
        'total_balance': str(category.total_balance + category.balance),
        'balance': str(category.balance),
        'iconCls': icon,
        'children': children}
    
  def _handle_search(self, categories):
    categories_return = []
    for category in categories:
      categories_return.append({
          'id': category.id,
          'name': category.name,
          'full_name': category.full_name})
    return categories_return


@require_auth
@require_POST
def move(request):
  wealth = request.session['wealth']
  try:
    params = load_params(request)
  except ValueError:
    return HttpResponse(JSON_FAILURE % 'Invalid arguments')
  form = CategoryMoveForm(
      params,
      wealth=wealth)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)
