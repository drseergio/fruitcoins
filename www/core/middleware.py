# -*- coding: utf-8 -*-
from django.utils.html import strip_spaces_between_tags
import re
from settings import COMPRESS_HTML
 
RE_MULTISPACE = re.compile(r'\s{2,}')
RE_NEWLINE = re.compile(r'\n')

 
class MinifyHTMLMiddleware(object):
  def process_response(self, request, response):
    if 'text/html' in response['Content-Type'] and COMPRESS_HTML:
      response.content = strip_spaces_between_tags(response.content.strip())
      response.content = RE_MULTISPACE.sub(' ', response.content)
      response.content = RE_NEWLINE.sub('', response.content)
    return response
