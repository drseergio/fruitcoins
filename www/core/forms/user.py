# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.forms import CharField
from django.forms import EmailField
from django.forms import ModelChoiceField
from django.forms import ValidationError
from django.forms.util import ErrorList
from core.forms import MoneypitForm
from core.logic.user import create_default_categories
from core.models import InviteRequest
from core.models import User
from core.models import Wealth
from emailconfirmation.models import EmailAddress
from fx.models import Currency
from recaptcha.client import captcha
from settings import CAPTCHA
from settings import DEBUG
from settings import RECAPTCHA_PRIVATE_KEY


class CreateUserForm(UserCreationForm):
  email = EmailField(required=False)
  recaptcha_response_field = CharField(required=False)


class CreateUserForm(UserCreationForm):
  email = EmailField(required=False)
  recaptcha_response_field = CharField(required=False)
  recaptcha_challenge_field = CharField(required=False)

  def __init__(self, *args, **kwargs):
    super(UserCreationForm, self).__init__(*args, **kwargs)
    self.fields['currency'] = ModelChoiceField(
        queryset=Currency.objects.all())

  def clean(self):
    super(UserCreationForm, self).clean()
    if self.errors:
      raise ValidationError('Basic validation has failed')
    if CAPTCHA:  # reCAPTCHA works on production
      recaptcha_response_value = self.cleaned_data['recaptcha_response_field']
      recaptcha_challenge_value = self.cleaned_data['recaptcha_challenge_field']
      check_captcha = captcha.submit(
          recaptcha_challenge_value,
          recaptcha_response_value,
          RECAPTCHA_PRIVATE_KEY, {})
      if not check_captcha.is_valid:
        self.add_error('recaptcha_response_field', 'Try captcha again')
    return self.cleaned_data

  def add_error(self, field, message):
    if field not in self._errors:
      self._errors[field] = ErrorList()
    self._errors[field].append(message)

  def save(self, request):
    UserCreationForm.save(self)
    user = auth.authenticate(
        username=self.cleaned_data['username'],
        password=self.cleaned_data['password1'])

    if self.cleaned_data['email']:
      email = self.cleaned_data['email']
      EmailAddress.objects.add_email(user, email)
    wealth = Wealth(
        user=user,
        currency=self.cleaned_data['currency'],
        balance=0)
    wealth.save()
    create_default_categories(wealth)

    auth.login(request, user)


class InviteUserForm(MoneypitForm):
  email = EmailField(required=False)
  recaptcha_response_field = CharField(required=False)
  recaptcha_challenge_field = CharField(required=False)

  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      InviteRequest.objects.get(email=email)
      raise ValidationError('This e-mail is already pending invitation')
    except ObjectDoesNotExist:
      pass
    return email

  def clean(self):
    super(InviteUserForm, self).clean()
    if CAPTCHA:  # reCAPTCHA works on production
      recaptcha_response_value = self.cleaned_data['recaptcha_response_field']
      recaptcha_challenge_value = self.cleaned_data['recaptcha_challenge_field']
      check_captcha = captcha.submit(
          recaptcha_challenge_value,
          recaptcha_response_value,
          RECAPTCHA_PRIVATE_KEY, {})
      if not check_captcha.is_valid:
        self.add_error('recaptcha_response_field', 'Try captcha again')
    return self.cleaned_data

  def save(self):
    invitation = InviteRequest(
        date=datetime.now(),
        email=self.cleaned_data['email'])
    invitation.save()


class CreateWealthForm(MoneypitForm):
  username = CharField(required=False)

  def __init__(self, *args, **kwargs):
    super(CreateWealthForm, self).__init__(*args, **kwargs)
    self.fields['currency'] = ModelChoiceField(
        queryset=Currency.objects.all())

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      User.objects.get(username=username)
      raise ValidationError('Username already exists')
    except ObjectDoesNotExist:
      return username

  def save(self, request):
    wealth = Wealth(
        user=request.user,
        currency=self.cleaned_data['currency'],
        balance=0)
    wealth.save()
    request.session['wealth'] = wealth
    create_default_categories(wealth)
    if self.cleaned_data['username']:
      user = request.user
      user.username = self.cleaned_data['username']
      user.save()


class ChangeUserForm(MoneypitForm):
  old_password = CharField()
  new_password1 = CharField(required=False)
  new_password2 = CharField(required=False)
  email = EmailField(required=False)

  def __init__(self, user, *args, **kwargs):
    self.user = user
    super(ChangeUserForm, self).__init__(*args, **kwargs)

  def clean_old_password(self):
    if not self.user.check_password(self.cleaned_data['old_password']):
      raise ValidationError('Old password is wrong')
    return self.cleaned_data['old_password']

  def clean(self):
    super(ChangeUserForm, self).clean()
    if self.cleaned_data['new_password1']:
      if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
        self.add_error('new_password1', 'New password does not match "repeat"')
    return self.cleaned_data

  def save(self):
    if self.cleaned_data['new_password1']:
      self.user.set_password(self.cleaned_data['new_password1'])
    if self.cleaned_data['email']:
      EmailAddress.objects.add_email(self.user, self.cleaned_data['email'])
    self.user.save()
