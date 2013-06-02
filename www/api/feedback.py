# -*- coding: utf-8 -*-
from api import get_json_errors
from api import JSON_SUCCESS
from api.decorators import require_auth
from core.forms.feedback import FeedbackForm
from core.models import Feedback
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.http import require_POST
from piston.handler import BaseHandler
from piston.utils import rc


@require_auth
@require_POST
def feedback(request):
  wealth = request.session['wealth']
  form = FeedbackForm(
      request.POST,
      wealth=wealth)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)
