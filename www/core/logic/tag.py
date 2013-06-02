# -*- coding: utf-8 -*-
from core.models import Tag
from core.models import TagSplit


def delete(tag):
  splits = TagSplit.objects.filter(tag=tag)
  for split in splits:
    split.delete()
  tag.delete()
