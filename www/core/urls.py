# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns(
  'core.views',
  (r'^$', 'app.index'))

urlpatterns += patterns('core.views.user',
    (r'^inviteme$', 'invite'),
    (r'^user/login$', 'login'),
    (r'^user/logout$', 'logout'),
    (r'^user/reset$', 'reset'),
    (r'^user/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'reset_password'),
    (r'^user/currency$', 'currency'),
    (r'^user/register$', 'register'))
