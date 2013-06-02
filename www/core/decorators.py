# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from core.models import Wealth
from logging import getLogger
from re import sub
from settings import CURRENCY_URL
from settings import LOGOUT_URL

logger = getLogger('core')


def check_wealth(orig_func):
  def check(*args, **kwargs):
    request = args[0]
    if request.user.is_authenticated():
      try:
        Wealth.objects.get(user=request.user)
      except ObjectDoesNotExist:
        logger.info('User %s is missing wealth' % request.user)
        return HttpResponseRedirect('/user/currency')
    return orig_func(*args, **kwargs)

  return check


def redirect_mobile(orig_func):
  def check(*args, **kwargs):
    request = args[0]
    if request.mobile:
      destination = sub(r'^/', '/mobile/', request.path)
      return HttpResponseRedirect(destination)
    return orig_func(*args, **kwargs)

  return check
