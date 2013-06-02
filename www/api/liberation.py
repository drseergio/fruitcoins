# -*- coding: utf-8 -*-
from api.decorators import require_auth
from api import get_json_errors
from api import get_json_error_response
from api import JSON_FAILURE
from api import JSON_SUCCESS
from celery.states import PENDING
from celery.states import STARTED
from core.forms.liberation import ImportForm
from core.models import WealthTask
from cStringIO import StringIO
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from djcelery.models import TaskMeta
from exporter.kmy import export
from gzip import GzipFile
from importer import commit_task
from importer import run_importers
from logging import getLogger
from piston.handler import BaseHandler

logger = getLogger('api')


@csrf_exempt
@require_auth
@require_POST
def upload(request):
  wealth = request.session['wealth']

  if 'importer' in request.session:
    return HttpResponse(JSON_FAILURE % 'Discard old data first')
  if _is_task_running(wealth):
    return HttpResponse(JSON_FAILURE % 'Import is already running')

  form = ImportForm(
      request.POST,
      request.FILES)
  if form.is_valid():
    try:
      request.session['importer'] = run_importers(
          wealth,
          request.FILES['importdata'],
          ['kmy'])
      return HttpResponse(JSON_SUCCESS)
    except Exception, e:
      logger.info(e)
      return get_json_error_response(e)
  else:
    return get_json_errors(form.errors)


@require_auth
@require_POST
def discard(request):
  if 'importer' in request.session:
    del request.session['importer']
    return HttpResponse(JSON_SUCCESS)
  else:
    return HttpResponse(JSON_FAILURE % 'Nothing to discard')


@require_auth
@require_POST
def progress(request):
  if 'importer' in request.session:
    return HttpResponse(JSON_FAILURE % 'Import not running')
  wealth = request.session['wealth']
  if _is_task_running(wealth):
    return HttpResponse(JSON_FAILURE % 'Import running')
  else:
    return HttpResponse(JSON_SUCCESS)


@require_auth
@require_POST
@transaction.commit_manually
def commit(request):
  if not 'importer' in request.session:
    return HttpResponse(JSON_FAILURE % 'Nothing to import')
  else:
    importer = request.session['importer']
    wealth = request.session['wealth']

    del request.session['importer']
    wealth_task = WealthTask(wealth=wealth, name='%d-import' % wealth.id)
    wealth_task.save()
    transaction.commit()
    commit_task.apply_async([wealth, importer], task_id='%d-import' % wealth.id)
    return HttpResponse(JSON_SUCCESS)


@require_auth
def export_kmy(request):
  wealth = request.session['wealth']
  xml = export(wealth)

  zbuf = StringIO()
  zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
  zfile.write(xml)
  zfile.close()
  compressed_content = zbuf.getvalue()

  response = HttpResponse(compressed_content, content_type='application/gzip')
  response['Content-Encoding'] = 'gzip'
  response['Content-Disposition'] = 'attachment; filename=moneypit-export-%s.kmy' % datetime.now().strftime('%Y-%m-%d')
  response['Content-Length'] = str(len(compressed_content))

  return response


def _is_task_running(wealth):
  task_id = '%d-import' % wealth.id
  try:
    task = WealthTask.objects.get(
        wealth=wealth,
        name=task_id)
    try:
      task_meta = TaskMeta.objects.get(task_id=task_id)
      if task_meta.status != PENDING and task_meta.status != STARTED:
        task.delete()
        return False
      else:
        return True
    except ObjectDoesNotExist:
      return True
  except ObjectDoesNotExist:
    return False


class ImportHandler(BaseHandler):
  def read(self, request):
    if 'importer' in request.session:
      importer = request.session['importer']
      return {'items': importer.get_preview()}
    else:
      return []
