# -*- coding: utf-8 -*-
from core.logic.user import wealth_exists
from django.http import HttpResponseRedirect
from logging import getLogger

logger = getLogger('api')


def new_user_handler(sender, user, request, **kwargs):
  if not wealth_exists(request):
    return HttpResponseRedirect('/user/currency')
  return None
