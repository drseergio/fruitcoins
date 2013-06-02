# -*- coding: utf-8 -*-
from api import load_params
from api.decorators import require_auth
from api.decorators import require_args
from api.decorators import require_pager
from api import get_json_errors
from api import get_json_error_response
from api import JSON_SUCCESS
from core.logic import get_date_period
from core.logic import get_list
from core.forms.liberation import ImportForm
from core.forms.transaction import AssociateTagForm
from core.forms.transaction import DeAssociateTagsForm
from core.forms.transaction import TransactionAddNonTransferForm
from core.forms.transaction import TransactionAddTransferForm
from core.forms.transaction import TransactionEditNonTransferForm
from core.forms.transaction import TransactionEditTransferForm
from core.logic.transaction import delete as delete_transaction
from core.logic.transaction import get_from_splits
from core.models import Account
from core.models import AccountSplit
from core.models import Category
from core.models import CategorySplit
from core.models import Tag
from core.models import TagSplit
from core.models import Transaction
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from exporter.seeesvee import export as export_csv
from importer import run_importers
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.transaction')


class TransactionHandler(BaseHandler):
  model = Transaction

  @require_args(['limit', 'start'], 'GET')
  @require_pager
  def read(self, request, transaction_type, object_id=None):
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])
    wealth = request.session['wealth']

    if not object_id and 'id' in request.GET:
      object_id = request.GET['id']
    if not object_id and transaction_type != 'wealth':
      return rc.BAD_REQUEST

    try:
      splits, name = _select_splits(transaction_type, object_id, wealth)
    except ValueError:
      return rc.BAD_REQUEST

    paged_splits = self._get_paged_splits(splits, start, limit)
    transactions = get_from_splits(paged_splits)

    return self._handle_transactions(transactions, len(splits))

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = load_params(request)

    accounts_list = get_list(Account.objects, wealth)

    if params['type'] == Transaction.TYPE_TRANSFER:
      form = TransactionAddTransferForm(params,
          wealth=wealth,
          accounts_list=accounts_list)
    else:
      if 'tags' in params:
        params['tags'] = self._get_tag_ids(params['tags'])
      tag_list=[(tag.id, tag.name)
          for tag in Tag.objects.filter(wealth=wealth)]
      categories_list = get_list(Category.objects, wealth)
      form = TransactionAddNonTransferForm(params,
          wealth=wealth,
          categories_list=categories_list,
          accounts_list=accounts_list,
          tag_list=tag_list)

    if form.is_valid():
      transaction = form.save()
      return {'success': True, 'id': transaction.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, transaction_type, object_id):
    wealth = request.session['wealth']
    transaction = Transaction.objects.get(
        wealth=wealth,
        id=object_id)
    delete_transaction(transaction)
    return {'success': True}

  @transaction.commit_on_success
  def update(self, request, transaction_type, object_id):
    params = load_params(request)
    wealth = request.session['wealth']
    params['id'] = object_id

    transaction = Transaction.objects.get(
        wealth=wealth,
        id=object_id)

    accounts_list = get_list(Account.objects, wealth)

    if 'type' not in params:
      resp = rc.BAD_REQUEST
      resp.write("'type' is a compulsory argument")
      return resp

    if params['type'] == Transaction.TYPE_TRANSFER:
       form = TransactionEditTransferForm(
          params,
          wealth=wealth,
          accounts_list=accounts_list)
    else:
      categories_list = get_list(Category.objects, wealth)
      form = TransactionEditNonTransferForm(
          params,
          wealth=wealth,
          categories_list=categories_list)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _get_paged_splits(self, splits, start, limit):
    page = start / limit + 1
    paginator = Paginator(splits, limit)
    try:
      paged_splits = paginator.page(page).object_list
    except EmptyPage:
      paged_splits = paginator.page(paginator.num_pages).object_list
    return paged_splits

  def _handle_transactions(self, transactions, total):
    transactions_return = []
    for transaction in transactions:
      transactions_return.append({
        'id': transaction.id,
        'date': str(transaction.date),
        'period': get_date_period(transaction.date),
        'category': transaction.category,
        'category_id': transaction.category_id,
        'description': transaction.description,
        'type': transaction.type,
        'tags': transaction.tags,
        'amount': str(abs(transaction.split.amount)),
        'amount_real': str(transaction.split.amount)})
    return {'total': total, 'items': transactions_return}

  def _get_tag_ids(self, tags):
    tags_return = []
    for tag in tags:
      try:
        tags_return.append(int(tag['id']))
      except ValueError:
        pass  # ignore invalid tags
    return tags_return


@transaction.commit_on_success
@require_auth
@require_POST
def tag(request):
  wealth = request.session['wealth']
  params = load_params(request)
  form = AssociateTagForm(
      params,
      wealth=wealth)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@transaction.commit_on_success
@require_auth
@require_POST
def remove_tags(request):
  wealth = request.session['wealth']
  params = load_params(request)
  form = DeAssociateTagsForm(
      params,
      wealth=wealth)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_auth
@require_GET
@require_args(['type'], 'GET', False)
def csv(request):
  wealth = request.session['wealth']
  view_type = request.GET['type']
  object_id = None

  if view_type != 'wealth':
    if not 'id' in request.GET:
      return HttpResponse(JSON_FAILURE % 'id is required')
    object_id = request.GET['id']

  try:
    splits, name = _select_splits(view_type, object_id, wealth)
  except ValueError:
    return rc.BAD_REQUEST
  return export_csv(wealth, splits, view_type, name)


@csrf_exempt
@require_auth
@require_POST
def upload(request, account_id):
  wealth = request.session['wealth']
  form = ImportForm(
      request.POST,
      request.FILES)
  if form.is_valid():
    try:
      account = Account.objects.get(wealth=wealth, id=account_id)
      importer = run_importers(
          wealth,
          request.FILES['importdata'],
          ['csv', 'qif'],
          account)
      importer.save()
      return HttpResponse(JSON_SUCCESS)
    except Exception, e:
      return get_json_error_response(e)
  else:
    return get_json_errors(form.errors)


def _select_splits(view_type, object_id, wealth):
  if view_type == 'wealth':
    splits = AccountSplit.objects.filter(
        ~Q(type=Transaction.TYPE_TRANSFER),
        wealth=wealth).order_by('-date')
    name = 'wealth'
  elif view_type == 'account':
    account = Account.objects.get(
        id=object_id,
        wealth=wealth)

    splits = AccountSplit.objects.filter(
        account=account,
        wealth=wealth).order_by('-date')
    name = account.name
  elif view_type == 'category':
    category = Category.objects.get(
        id=object_id,
        wealth=wealth)

    splits = CategorySplit.objects.filter(
        category=category,
        wealth=wealth).order_by('-date')
    name = category.name
  elif view_type == 'tag':
    tag = Tag.objects.get(
        id=object_id,
        wealth=wealth)

    splits = TagSplit.objects.filter(
        tag=tag,
        wealth=wealth).order_by('-date')
    name = tag.name
  else:
    raise ValueError
  return splits, name
