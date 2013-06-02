# -*- coding: utf-8 -*-
from django.forms import CharField
from django.forms import IntegerField
from django.forms import ValidationError
from core.forms import MoneypitForm
from core.models import Budget
from time import strptime


class BudgetAddForm(MoneypitForm):
  name = CharField()
  year = IntegerField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(BudgetAddForm, self).__init__(*args, **kwargs)

  def clean_year(self):
    year = self.cleaned_data['year']
    try:
      strptime('1/1/%d' % year, '%m/%d/%Y')
    except ValueError:
      raise ValidationError('Invalid year specification')
    return year

  def save(self):
    budget = Budget(
        wealth=self.wealth,
        name=self.cleaned_data['name'],
        year=self.cleaned_data['year'])
    budget.save()
    return budget
