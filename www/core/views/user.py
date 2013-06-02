# -*- coding: utf-8 -*-
from core.decorators import redirect_mobile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from fx import detect_currency
from logging import getLogger
from settings import CAPTCHA
from settings import DEBUG
from settings import INVITE_ONLY

logger = getLogger('core')


@redirect_mobile
def login(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  else:
    if 'next' in request.GET:
      destination = request.GET['next']
    else:
      destination = '/'
    return render_to_response(
        'login.html',
        {'next': destination, 'debug': DEBUG, 'invite': INVITE_ONLY},
        context_instance=RequestContext(request))


@login_required
def currency(request):
  if 'wealth' in request.session:
    return HttpResponseRedirect('/')
  debug = DEBUG
  currency_id = detect_currency(request)
  return render_to_response(
      'currency.html',
      {'debug': DEBUG, 'currency': currency_id},
      context_instance=RequestContext(request))


@login_required
def logout(request):
  auth.logout(request)
  return HttpResponseRedirect("/user/login")


def invite(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  if not INVITE_ONLY:
    return HttpResponseRedirect('/')
  debug = DEBUG
  captcha = CAPTCHA
  return render_to_response(
      'invite.html',
      locals(),
      context_instance=RequestContext(request))


def register(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  if INVITE_ONLY:
    return HttpResponseRedirect('/')
  debug = DEBUG
  currency_id = detect_currency(request)
  return render_to_response(
      'register.html',
      {'debug': DEBUG, 'captcha': CAPTCHA, 'currency': currency_id},
      context_instance=RequestContext(request))


def reset(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  debug = DEBUG
  return render_to_response(
      'reset.html',
      locals(),
      context_instance=RequestContext(request))


def reset_password(request, uidb36, token):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  debug = DEBUG
  return render_to_response(
      'reset_password.html',
      locals(),
      context_instance=RequestContext(request))
