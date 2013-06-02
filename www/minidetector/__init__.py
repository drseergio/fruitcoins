# -*- coding: utf-8 -*-

from useragents import search_strings


class Middleware(object):
  @staticmethod
  def process_request(request):
    if request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
      request.mobile = True
      return None

    if request.META.has_key("HTTP_ACCEPT"):
      s = request.META["HTTP_ACCEPT"].lower()
      if 'application/vnd.wap.xhtml+xml' in s:
        request.mobile = True
        return None

    if request.META.has_key("HTTP_USER_AGENT"):
      s = request.META["HTTP_USER_AGENT"].lower()
      for ua in search_strings:
        if ua in s:
          request.mobile = True
          return None

    request.mobile = False
    return None


def detect_mobile(view):
  def detected(request, *args, **kwargs):
    Middleware.process_request(request)
    return view(request, *args, **kwargs)
  detected.__doc__ = "%s\n[Wrapped by detect_mobile which detects if the request is from a phone]" % view.__doc__
  return detected


__all__ = ['Middleware', 'detect_mobile']
