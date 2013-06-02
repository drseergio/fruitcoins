# -*- coding: utf-8 -*-
from api import load_params
from api.decorators import require_args
from core.forms.account import AccountAddForm
from core.forms.account import AccountEditForm
from core.logic.account import delete as delete_account
from core.models import Account
from django.db import transaction
from django.db.models import Q
from django.utils import simplejson
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api')


class AccountHandler(BaseHandler):
  model = Account

  def read(self, request, account_id=None, search=None):
    wealth = request.session['wealth']
    base = Account.objects

    if account_id:
      return self._handle_get(base.get(
          wealth=wealth,
          id=account_id))
    elif 'query' in request.GET and search:
      return self._handle_search(base.filter(
          wealth=wealth,
          name__icontains=request.GET['query']))
    else:
      return self._handle_index(base.filter(
          wealth=wealth).order_by('type'))

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = load_params(request)

    form = AccountAddForm(params, wealth=wealth)
    if form.is_valid():
      account = form.save()
      return {'success': True, 'id': account.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def update(self, request, account_id):
    wealth = request.session['wealth']
    params = load_params(request)
    params['id'] = account_id

    account = Account.objects.get(
        wealth=wealth,
        id=account_id)

    form = AccountEditForm(
        params,
        wealth=wealth)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, account_id):
    wealth = request.session['wealth']

    account = Account.objects.get(
        wealth=wealth,
        id=account_id)
    delete_account(account)
    return {'success': True}

  def _handle_get(self, account):
    return {
        'type': account.type,
        'name': account.name,
        'id': account.id,
        'opened_date': str(account.opened_date),
        'description': account.description,
        'currency': account.currency.symbol,
        'balance': str(account.balance)}

  def _handle_index(self, accounts):
    accounts_return = []
    for account in accounts:
      accounts_return.append({
          'id': account.id,
          'name': account.name,
          'currency': account.currency.symbol,
          'type': account.type,
          'balance': str(account.balance)})
    return accounts_return

  def _handle_search(self, accounts):
    accounts_return = []
    for account in accounts:
      accounts_return.append({
          'id': account.id,
          'name': account.name,
          'currency': account.currency.symbol})
    return accounts_return
