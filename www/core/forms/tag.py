# -*- coding: utf-8 -*-
from datetime import datetime
from django.forms import CharField
from django.forms import ModelChoiceField
from core.forms import MoneypitForm
from core.models import Tag


class TagAddForm(MoneypitForm):
  name = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(TagAddForm, self).__init__(*args, **kwargs)

  def save(self):
    tag = Tag(
        wealth=self.wealth,
        name=self.cleaned_data['name'],
        modified_date=datetime.utcnow(),
        created_date=datetime.utcnow())
    tag.save()
    return tag


class TagEditForm(MoneypitForm):
  name = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(TagEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(
        queryset=Tag.objects.filter(wealth=self.wealth))

  def save(self):
    tag = self.cleaned_data['id']
    tag.name = self.cleaned_data['name']
    tag.save()
