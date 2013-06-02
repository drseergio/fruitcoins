# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class TagEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['tag', 'tag/331'])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/tag')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

  def test_empty_account(self):
    response = self.run_get('fred', '/api/tag/55')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/tag/*(&$@*&(')
    self.assertEquals(response.status_code, 404)


class TagReadTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_tag']

  def test_fred_index(self):
    response = self.run_get('fred', '/api/tag')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)

  def test_mary_index(self):
    response = self.run_get('mary', '/api/tag')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)

  def test_unauthorized(self):
    response = self.run_get('fred', '/api/tag/71')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('mary', '/api/tag/71')
    self.assertEquals(response.status_code, 200)


class TagAddTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_tag']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/tag')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'name': 'New World Order'})
    response = self.run_post(
        'fred',
        '/api/tag',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)
    tag_id = result['id']

    response = self.run_get('fred', '/api/tag/%s' % tag_id)
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'New World Order')


class TagDeleteTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_tag']

  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/tag/1066')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/tag/71')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/tag/70')
    self.assertEquals(response.status_code, 200)

    response = self.run_delete('fred', '/api/tag/70')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/tag/70')
    self.assertEquals(response.status_code, 404)


class TagUpdateTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_tag']

  def test_no_arguments(self):
    response = self.run_put('fred', '/api/tag/70')
    self.assertEquals(response.status_code, 400)

  def test_unauthorized(self):
    data = simplejson.dumps({'name': 'workamongous'})
    response = self.run_put(
        'fred',
        '/api/tag/71',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    data = simplejson.dumps({
        'name': 'New World Order' })
    response = self.run_put(
        'fred',
        '/api/tag/70',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/tag/70')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'New World Order')
