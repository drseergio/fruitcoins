# -*- coding: utf-8 -*-
from core.decorators import check_wealth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from fx.decorators import check_rates
from settings import ANALYTICS_ID
from settings import DEBUG
from settings import DEFAULT_TRANSACTIONS_PER_PAGE
from social_auth.models import UserSocialAuth


def login(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/mobile')
  else:
    if 'next' in request.GET:
      destination = request.GET['next']
    else:
      destination = '/mobile'
    return render_to_response(
        'mobile-login.html',
        {'next': destination, 'debug': DEBUG},
        context_instance=RequestContext(request))


@login_required
@check_wealth
@check_rates
def app(request):
  wealth = request.session['wealth']
  try:
    UserSocialAuth.objects.get(user=request.user)
    social = True
  except ObjectDoesNotExist:
    social = False
  return render_to_response(
      'mobile-app.html', {
          'analytics': ANALYTICS_ID,
          'debug': DEBUG,
          'social': social,
          'perpage': DEFAULT_TRANSACTIONS_PER_PAGE,
          'currency': wealth.currency },
      context_instance=RequestContext(request))
