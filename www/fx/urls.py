# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns(
  'fx.views',
  (r'^rate$', 'get'))
