# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CharField
from django.forms import ModelChoiceField
from django.forms import ValidationError
from core.forms import MoneypitForm
from core.logic.category import change_type
from core.models import Category


class CategoryAddForm(MoneypitForm):
  text = CharField(required=False)
  description = CharField(required=False)
  parent = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(CategoryAddForm, self).__init__(*args, **kwargs)

  def clean_text(self):
    name = self.cleaned_data['text']
    if ':' in name:
      raise ValidationError('Name cannot contain colon')
    return name

  def clean_parent(self):
    parent = self.cleaned_data['parent']
    if parent == 'inc':
      self.category_type = Category.TYPE_INCOME
    elif parent == 'exp':
      self.category_type = Category.TYPE_EXPENSE
    else:
      try:
        parent = Category.objects.get(
            wealth=self.wealth,
            id=parent)
        self.category_type = parent.type
      except ObjectDoesNotExist:
        raise ValidationError('Please select a valid choice')
    return parent

  def save(self):
    parent = self.cleaned_data['parent']
    if parent == 'inc' or parent == 'exp':
      parent = None

    category = Category(
        wealth=self.wealth,
        type=self.category_type,
        parent=parent,
        name=self.cleaned_data['text'],
        description=self.cleaned_data['description'],
        balance=0,
        total_balance=0)
    category.save()
    return category


class CategoryEditForm(MoneypitForm):
  text = CharField()
  description = CharField(required=False)

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(CategoryEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(
        queryset=Category.objects.filter(wealth=self.wealth))

  def save(self):
    category = self.cleaned_data['id']
    category.name = self.cleaned_data['text']
    category.description = self.cleaned_data['description']
    category.save()


class CategoryMoveForm(MoneypitForm):
  new_parent = CharField()
  old_parent = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(CategoryMoveForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(
        queryset=Category.objects.filter(wealth=self.wealth))
    self.category_type = {}

  def clean_new_parent(self):
    return self._clean_parent('new_parent')

  def clean_old_parent(self):
    return self._clean_parent('old_parent')

  def _clean_parent(self, field):
    parent = self.cleaned_data[field]
    if parent == 'inc':
      self.category_type[field] = Category.TYPE_INCOME
    elif parent == 'exp':
      self.category_type[field] = Category.TYPE_EXPENSE
    else:
      try:
        parent = Category.objects.get(
            wealth=self.wealth,
            id=parent)
        self.category_type[field] = parent.type
      except ObjectDoesNotExist:
        raise ValidationError('Please select a valid choice')
    return parent

  def save(self):
    category = self.cleaned_data['id']
    type_changed = False

    if self.category_type['new_parent'] != self.category_type['old_parent']:
      type_changed = True

    new_parent = self.cleaned_data['new_parent']
    if new_parent == 'inc' or new_parent == 'exp':
      new_parent = None

    old_parent = self.cleaned_data['old_parent']
    if old_parent == 'inc' or old_parent == 'exp':
      old_parent = None

    category.parent = new_parent
    category.type = self.category_type['new_parent']
    category.save()

    if new_parent:
      new_parent.calculate_total_balance()

    if old_parent:
      old_parent.calculate_total_balance()

    if type_changed:
      change_type(category, category.type)
