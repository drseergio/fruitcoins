# -*- coding: utf-8 -*-
from core.decorators import check_wealth
from core.decorators import redirect_mobile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from fx.decorators import check_rates
from settings import ANALYTICS_ID
from settings import DEBUG
from settings import DEFAULT_TRANSACTIONS_PER_PAGE
from social_auth.models import UserSocialAuth


@redirect_mobile
@login_required
@check_wealth
@check_rates
def index(request):
  wealth = request.session['wealth']
  try:
    UserSocialAuth.objects.get(user=request.user)
    social = True
  except ObjectDoesNotExist:
    social = False
  return render_to_response(
      'app.html', {
          'analytics': ANALYTICS_ID,
          'debug': DEBUG,
          'social': social,
          'perpage': DEFAULT_TRANSACTIONS_PER_PAGE,
          'currency': wealth.currency },
      context_instance=RequestContext(request))
