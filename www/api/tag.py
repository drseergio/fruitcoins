# -*- coding: utf-8 -*-
from core.forms.tag import TagAddForm
from core.forms.tag import TagEditForm
from core.logic.tag import delete as delete_tag
from core.models import Tag
from django.db import transaction
from django.db.models import Q
from django.utils import simplejson
from piston.handler import BaseHandler
from piston.utils import rc


class TagHandler(BaseHandler):
  model = Tag

  def read(self, request, tag_id=None):
    wealth = request.session['wealth']
    base = Tag.objects

    if tag_id:
      return self._handle_get(base.get(
          wealth=wealth,
          id=tag_id))
    else:
      tags = base.filter(wealth=wealth).order_by('-modified_date')
      return self._handle_index(tags)

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    wealth = request.session['wealth']
    params = simplejson.loads(request.raw_post_data)

    form = TagAddForm(params, wealth=wealth)
    if form.is_valid():
      tag = form.save()
      return {'success': True, 'id': tag.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def update(self, request, tag_id):
    wealth = request.session['wealth']
    params = simplejson.loads(request.raw_post_data)
    params['id'] = tag_id

    tag = Tag.objects.get(
        wealth=wealth,
        id=tag_id)

    form = TagEditForm(
        params,
        wealth=wealth)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, tag_id):
    wealth = request.session['wealth']

    tag = Tag.objects.get(
        wealth=wealth,
        id=tag_id)
    delete_tag(tag)
    return {'success': True}

  def _handle_index(self, tags):
    tags_return = []
    for tag in tags:
      tags_return.append({
          'id': tag.id,
          'name': tag.name,
          'created_date': str(tag.created_date),
          'modified_date': str(tag.modified_date),
          'balance': str(tag.balance)})
    return tags_return

  def _handle_get(self, tag):
    return {
        'name': tag.name,
        'id': tag.id,
        'created_date': str(tag.created_date),
        'modified_date': str(tag.modified_date),
        'balance': str(tag.balance)}
