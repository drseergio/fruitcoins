# -*- coding: utf-8 -*-
from api import get_json_errors
from api import JSON_SUCCESS
from api.decorators import require_args
from api.decorators import require_auth
from core.forms.receipt import UploadForm
from core.models import Receipt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from filetransfers.api import serve_file
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api')


@csrf_exempt
@require_auth
@require_args(['image'], 'POST', False)
@require_POST
def upload(request):
  wealth = request.session['wealth']

  form = UploadForm(request.POST, wealth=wealth)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_auth
@require_args(['id'], 'GET', False)
def image(request):
  wealth = request.session['wealth']
  try:
    receipt = Receipt.objects.get(wealth=wealth, id=request.GET['id'])
    return serve_file(request, receipt.image)
  except ObjectDoesNotExist:
    return rc.NOT_FOUND


class ReceiptHandler(BaseHandler):
  allowed_methods = ('GET', 'DELETE')
  model = Receipt

  def read(self, request, receipt_id=None):
    wealth = request.session['wealth']
    base = Receipt.objects

    if receipt_id:
      return self._handle_get(base.get(
          wealth=wealth,
          id=receipt_id))
    else:
      receipts = base.filter(wealth=wealth).order_by('-date')
      return self._handle_index(receipts)

  def delete(self, request, receipt_id):
    wealth = request.session['wealth']

    receipt = Receipt.objects.get(
        wealth=wealth,
        id=receipt_id)
    receipt.delete()
    return {'success': True}

  def _handle_index(self, receipts):
    receipts_return = []
    for receipt in receipts:
      receipts_return.append({
          'id': receipt.id,
          'date': str(receipt.date)})
    return receipts_return

  def _handle_get(self, receipt):
    return {
        'id': receipt.id,
        'date': str(receipt.date)}
