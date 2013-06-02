# -*- coding: utf-8 -*-
from core.models import Wealth
from django.core.exceptions import ObjectDoesNotExist
from piston.utils import rc


class NotFound(object):
  def process_exception(self, request, exception):
   if isinstance(exception, ObjectDoesNotExist):
     return rc.NOT_FOUND
   return None


class InsertWealth(object):
  def process_request(self, request):
    if request.user.is_authenticated() and 'wealth' not in request.session:
      raw = request.raw_post_data
      request.session['wealth'] = Wealth.objects.get(user=request.user)
      request.session.save()
