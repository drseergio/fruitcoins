# -*- coding: utf-8 -*-
from api import JSON_SUCCESS
from api import get_json_errors
from api import get_json_error_response
from api import str_handler
from api.decorators import require_args
from api.decorators import require_auth
from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.http import base36_to_int
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from core.forms.user import ChangeUserForm
from core.forms.user import CreateUserForm
from core.forms.user import CreateWealthForm
from core.forms.user import InviteUserForm
from core.signals import new_user_handler
from piston.utils import rc
from settings import INVITE_ONLY


@csrf_exempt
@require_POST
def login(request):
  user = auth.authenticate(
      username=request.POST['username'],
      password=request.POST['password'])

  if user and user.is_active:
      auth.login(request, user)
      return HttpResponse(JSON_SUCCESS)
  return get_json_error_response()


@require_POST
def register(request):
  if request.user.is_authenticated():
    return HttpResponse(status=400)

  if INVITE_ONLY:
    return get_json_errors(
        {'username': 'Registration is currently closed'},
        str_handler)

  form = CreateUserForm(request.POST)

  if form.is_valid():
    form.save(request)
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_POST
def invite(request):
  if request.user.is_authenticated():
    return HttpResponse(status=400)
  if not INVITE_ONLY:
    return HttpResponse(status=400)

  form = InviteUserForm(request.POST)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_POST
def reset(request):
  if request.user.is_authenticated():
    return HttpResponse(status=400)

  form = PasswordResetForm(request.POST)

  if form.is_valid():
    form.save(email_template_name='password_email.html')
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_POST
@require_args(['uidb36', 'token'], 'POST', False)
def reset_password(request):
  if request.user.is_authenticated():
    return HttpResponse(status=400)

  uidb36 = request.POST['uidb36']
  token = request.POST['token']

  try:
    uid_int = base36_to_int(uidb36)
    user = User.objects.get(id=uid_int)
  except (ValueError, ObjectDoesNotExist):
    user = None

  if user is not None and default_token_generator.check_token(user, token):
    form = SetPasswordForm(user, request.POST)
    if form.is_valid():
      form.save()
      user = auth.authenticate(
          username=user.username,
          password=request.POST['new_password1'])
      auth.login(request, user)
      return HttpResponse(JSON_SUCCESS)
    else:
      return get_json_errors(form.errors)
  else:
    return HttpResponse(status=400)


@require_auth
@require_POST
def change(request):
  form = ChangeUserForm(request.user, request.POST)
  if form.is_valid():
    form.save()
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


@require_auth
@require_POST
def currency(request):
  if 'wealth' in request.session:
    return HttpResponse(JSON_FAILURE % 'Already exists')

  form = CreateWealthForm(request.POST)

  if form.is_valid():
    form.save(request)
    return HttpResponse(JSON_SUCCESS)
  else:
    return get_json_errors(form.errors)


user_logged_in.connect(new_user_handler)
