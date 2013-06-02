# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns('mobile.views',
    (r'^$', 'app'),
    (r'^user/login$', 'login'))
