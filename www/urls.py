# coding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from settings import ADMIN_ENABLED


urlpatterns = patterns('',
    (r'', include('social_auth.urls')))

if ADMIN_ENABLED:
  admin.autodiscover()
  urlpatterns += patterns('',
      (r'^sentry/', include('sentry.web.urls')),
      (r'^admin/', include(admin.site.urls)))

urlpatterns += patterns('',
    (r'^confirm_email/(\w+)/$', 'emailconfirmation.views.confirm_email'))

urlpatterns += patterns('',
    (r'^api/', include('api.urls')),
    (r'^fx/', include('fx.urls')),
    (r'^mobile/', include('mobile.urls')),
    (r'^', include('core.urls')))

urlpatterns += staticfiles_urlpatterns()
