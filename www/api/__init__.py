# -*- coding: utf-8 -*-
from core.models import User
from core.models import Wealth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson
from django.utils.http import urlquote
from django.views.decorators.vary import vary_on_headers
from logging import getLogger
from settings import LOGIN_URL
from piston.emitters import Emitter
from piston.handler import typemapper
from piston.resource import CHALLENGE
from piston.resource import Resource
from piston.utils import coerce_put_post
from piston.utils import HttpStatusCode
from piston.utils import rc
from piston.utils import translate_mime
from piston.utils import MimerDataException

logger = getLogger('api')

JSON_SUCCESS = '{"success":true}'
JSON_FAILURE = '{"success":false,"message":"%s"}'
JSON_FAILURE_EMPTY = '{"success":false}'


def get_json_response(objects, handler=None, total=None):
  objects_envelope = []

  if handler:
    for obj in objects:
      objects_envelope.append(handler(obj))
  else:
    objects_envelope = objects

  if total:
    return_dict = {'count': total, 'items': objects_envelope}
  else:
    return_dict = {'count': len(objects_envelope), 'items': objects_envelope}

  return HttpResponse(simplejson.dumps(return_dict))


def load_params(request):
  try:
    return simplejson.loads(request.raw_post_data)
  except Exception:
    raise ValueError('invalid arguments')


def get_json_response_object(obj, handler):
  return HttpResponse(simplejson.dumps([handler(obj)]))


def form_handler(error):
  return error.as_text()


def str_handler(error):
  return error


def get_json_errors(errors, handler=form_handler):
  response = '{"success":false, "errors":['
  response += ','.join(['{"id":"%s","msg":"%s"}' % (field, handler(error))
    for field, error in errors.items()])
  response += ']}'
  return HttpResponse(status=200, content=response)


def get_json_error_response(message="", code=400):
  if message:
    content = JSON_FAILURE % message
  else:
    content = JSON_FAILURE_EMPTY
  return HttpResponse(status=code, content=content)


class ApiTestCase(TestCase):
  def auth_required(self, paths):
    for path in paths:
      response = self.client.get('/api/%s' % path)
      self.assertEquals(response.status_code, 401)
      response = self.client.post('/api/%s' % path)
      self.assertEquals(response.status_code, 401)
      response = self.client.put('/api/%s' % path)
      self.assertEquals(response.status_code, 401)
      response = self.client.delete('/api/%s' % path)
      self.assertEquals(response.status_code, 401)

  def run_get(self, username, path, data={}):
    c = Client()
    c.login(username=username, password='test')
    session = c.session
    user = User.objects.get(username=username)
    session['wealth'] = Wealth.objects.get(user=user)
    session.save()
    return c.get(path, data)

  def run_post(self, username, path, data={}, content_type=None):
    self.client.login(username=username, password='test')
    if content_type:
      return self.client.post(path, data, content_type)
    else:
      return self.client.post(path, data)

  def run_put(self, username, path, data={}, content_type=None):
    self.client.login(username=username, password='test')
    if content_type:
      return self.client.put(path, data, content_type)
    else:
      return self.client.put(path, data)

  def run_delete(self, username, path, data={}):
    self.client.login(username=username, password='test')
    return self.client.delete(path, data)


class DjangoAuthentication(object):
  def __init__(self, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    if not login_url:
      login_url = LOGIN_URL
    self.login_url = login_url
    self.redirect_field_name = redirect_field_name
    self.request = None

  def is_authenticated(self, request):
    self.request = request
    return request.user.is_authenticated()

  def challenge(self):
    return HttpResponse(status=401)


class MoneypitResource(Resource):
  def __init__(self, handler, authentication=None):
    super(MoneypitResource, self).__init__(handler, authentication)

  @vary_on_headers('Authorization')
  def __call__(self, request, *args, **kwargs):
    rm = request.method.upper()

    if rm == "PUT":
      coerce_put_post(request)

    actor, anonymous = self.authenticate(request, rm)

    if anonymous is CHALLENGE:
      return actor()
    else:
      handler = actor

    if rm in ('POST', 'PUT'):
      try:
        translate_mime(request)
      except MimerDataException:
        return rc.BAD_REQUEST
      if not hasattr(request, 'data'):
        if rm == 'POST':
          request.data = request.POST
        else:
          request.data = request.PUT

    if not rm in handler.allowed_methods:
      return HttpResponseNotAllowed(handler.allowed_methods)

    meth = getattr(handler, self.callmap.get(rm, ''), None)
    if not meth:
      raise Http404

    em_format = self.determine_emitter(request, *args, **kwargs)
    kwargs.pop('emitter_format', None)

    request = self.cleanup_request(request)

    try:
      result = meth(request, *args, **kwargs)
    except ValueError:
      result = rc.BAD_REQUEST
      result.content = 'Invalid arguments'

    try:
      emitter, ct = Emitter.get(em_format)
      fields = handler.fields
      if hasattr(handler, 'list_fields') and isinstance(result, (list, tuple, QuerySet)):
        fields = handler.list_fields
    except ValueError:
      result = rc.BAD_REQUEST
      result.content = "Invalid output format specified '%s'." % em_format
      return result

    status_code = 200

    if isinstance(result, HttpResponse) and not result._is_string:
      status_code = result.status_code
      result = result._container
     
    srl = emitter(result, typemapper, handler, fields, anonymous)

    try:
      if self.stream: stream = srl.stream_render(request)
      else: stream = srl.render(request)

      if not isinstance(stream, HttpResponse):
        resp = HttpResponse(stream, mimetype=ct, status=status_code)
      else:
        resp = stream
      resp.streaming = self.stream
      return resp
    except HttpStatusCode, e:
      return e.response
