# -*- coding: utf-8 -*-
from api.decorators import require_args
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from fx import get_rate


@login_required
@require_args(['from', 'to'], 'GET', False)
def get(request):
  symbol_from = request.GET['from']
  symbol_to = request.GET['to']

  return HttpResponse(get_rate(symbol_from, symbol_to))
