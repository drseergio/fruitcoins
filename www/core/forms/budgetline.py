# -*- coding: utf-8 -*-
from core.forms import MoneypitForm
from core.models import Budget
from core.models import BudgetLine
from core.models import Category
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ChoiceField
from django.forms import ModelChoiceField
from django.forms import DecimalField
from django.forms import ValidationError


class BudgetLineAddForm(MoneypitForm):
  period = ChoiceField(choices=BudgetLine.PERIODS)
  amount = DecimalField(initial=0.0)

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(BudgetLineAddForm, self).__init__(*args, **kwargs)

    self.fields['budget'] = ModelChoiceField(
        queryset=Budget.objects.filter(wealth=self.wealth))

    self.fields['category_id'] = ModelChoiceField(
        queryset=Category.objects.filter(wealth=self.wealth))

  def clean_amount(self):
    amount = self.cleaned_data['amount']
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount

  def clean(self):
    super(BudgetLineAddForm, self).clean()
    if not 'category_id' in self.cleaned_data:
      raise ValidationError('Category is required')
    category = self.cleaned_data['category_id']
    if not 'budget' in self.cleaned_data:
      raise ValidationError('Budget is required')
    budget = self.cleaned_data['budget']

    try:
      BudgetLine.objects.get(
          wealth=self.wealth,
          category=category,
          budget=budget)
      self.add_error('category_id', 'Budget line for this category already exists')
    except ObjectDoesNotExist:
      pass

    return self.cleaned_data

  def save(self):
    category = self.cleaned_data['category_id']
    budget = self.cleaned_data['budget']
    period = int(self.cleaned_data['period'])
    amount = self.cleaned_data['amount']

    line = BudgetLine(
        wealth=self.wealth,
        category=category,
        balance=0,
        type=category.type,
        total_amount=0,
        budget=budget,
        year=budget.year,
        period=period,
        amount=amount)

    line.save()
    return line

class BudgetLineEditForm(BudgetLineAddForm):
  def __init__(self, *args, **kwargs):
    super(BudgetLineEditForm, self).__init__(*args, **kwargs)

    self.fields['id'] = ModelChoiceField(
        queryset=BudgetLine.objects.filter(wealth=self.wealth))

  def clean(self):
    super(BudgetLineEditForm, self).clean()
    if not 'id' in self.cleaned_data:
      raise ValidationError('ID is required')
    budgetline = self.cleaned_data['id']
    return self.cleaned_data

  def save(self):
    amount = self.cleaned_data['amount']
    period = int(self.cleaned_data['period'])
    budgetline = self.cleaned_data['id']

    if 'category_id' in self.cleaned_data:
      category = self.cleaned_data['category_id']
      budgetline.category = category
      budgetline.type = category.type

    budgetline.amount = amount
    budgetline.period = period

    budgetline.save()
