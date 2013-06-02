# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class CategoryEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['category', 'category/331', 'category/search'])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/category')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

  def test_empty_category(self):
    response = self.run_get('fred', '/api/category/55')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/category/*(&$@*&(')
    self.assertEquals(response.status_code, 404)

  def test_empty_search(self):
    response = self.run_get('fred', '/api/category/search')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

    response = self.run_get('fred', '/api/category/search?query=@*&(#(*&*(@E!')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')


class CategoryReadTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_category']

  def test_whole_tree(self):
    response = self.run_get('fred', '/api/category?node=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result[0]['text'], 'Expense')
    self.assertEquals(result[0]['children'][0]['text'], 'Girls')
    self.assertEquals(result[1]['text'], 'Income')
    self.assertEquals(result[1]['children'][0]['text'], 'Salary')

  def test_node(self):
    response = self.run_get('fred', '/api/category?node=2000')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result[0]['text'], 'Crime')
    self.assertEquals(result[1]['text'], 'Crimeless')

  def test_unauthorized(self):
    response = self.run_get('fred', '/api/category?node=2005')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('mary', '/api/category?node=2005')
    self.assertEquals(response.status_code, 200)

  def test_search(self):
    response = self.run_get('fred', '/api/category/search?query=ime')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(len(result), 2)

  def test_success(self):
    response = self.run_get('fred', '/api/category/2000')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(result['text'], 'Salary')


class CategoryAddTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_category']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/category')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'text': 'workamongous',
        'description': 'whiz',
        'parent': 2000 })
    response = self.run_post(
        'fred',
        '/api/category',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)
    category_id = result['id']

    response = self.run_get(
        'fred',
        '/api/category/%s' % category_id)
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['text'], 'workamongous')


class CategoryDeleteTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_category']

  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/category/1066')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/category/2005')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/category/2000')
    self.assertEquals(response.status_code, 200)

    response = self.run_delete('fred', '/api/category/2000')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/category/2000')
    self.assertEquals(response.status_code, 404)


class CategoryUpdateTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_category']

  def test_no_arguments(self):
    response = self.run_put('fred', '/api/category/2000')
    self.assertEquals(response.status_code, 400)

  def test_unauthorized(self):
    data = simplejson.dumps({'text': 'workamongous'})
    response = self.run_put(
        'fred',
        '/api/category/2005',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    data = simplejson.dumps({
        'text': 'New World Order' })
    response = self.run_put(
        'fred',
        '/api/category/2000',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/category/2000')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['text'], 'New World Order')


class CategoryMoveTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_category']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/category/move')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], False)

  def test_success(self):
    data = simplejson.dumps({
        'id': 2006,
        'new_parent': 2003,
        'old_parent': 2000 })
    response = self.run_post(
        'fred',
        '/api/category/move',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/category?node=2000')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(len(result), 1)

    response = self.run_get('fred', '/api/category?node=2003')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result[0]['text'], 'Crimeless')
