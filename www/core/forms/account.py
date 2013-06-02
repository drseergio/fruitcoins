# -*- coding: utf-8 -*-
from datetime import datetime
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DateField
from django.forms import DecimalField
from django.forms import ModelChoiceField
from django.forms import ValidationError
from core.forms import MoneypitForm
from core.models import Account
from core.models import Currency


class AccountAddForm(MoneypitForm):
  name = CharField()
  type = ChoiceField(choices=Account.TYPES)
  opening_balance = DecimalField(initial=0.0, required=False)
  opened_date = DateField(initial=datetime.utcnow())

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(AccountAddForm, self).__init__(*args, **kwargs)
    self.fields['currency'] = ModelChoiceField(
        queryset=Currency.objects.all())

  def clean_opened_date(self):
    date = self.cleaned_data['opened_date']
    now = datetime.utcnow().date()
    if now < date:
      raise ValidationError('Cannot open account in future')
    return date

  def clean_opening_balance(self):
    balance = self.cleaned_data['opening_balance']
    if not balance:
      balance = 0
    return balance

  def save(self):
    account = Account(
        wealth=self.wealth,
        type=self.cleaned_data['type'],
        name=self.cleaned_data['name'],
        balance=self.cleaned_data['opening_balance'],
        modified_date=datetime.utcnow(),
        currency=self.cleaned_data['currency'],
        opening_balance=self.cleaned_data['opening_balance'],
        opened_date=self.cleaned_data['opened_date'])
    account.save()
    return account


class AccountEditForm(MoneypitForm):
  name = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(AccountEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(
        queryset=Account.objects.filter(wealth=self.wealth))

  def save(self):
    account = self.cleaned_data['id']
    account.name = self.cleaned_data['name']
    account.save()
