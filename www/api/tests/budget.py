# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class BudgetEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['budget', 'budget/331'])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/budget')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

  def test_empty_account(self):
    response = self.run_get('fred', '/api/budget/55')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/budget/*(&$@*&(')
    self.assertEquals(response.status_code, 404)


class BudgetReadTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_budget']

  def test_fred_index(self):
    response = self.run_get('fred', '/api/budget')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 2)
    account = result[0]
    self.assertEquals(account['name'], 'Victor')
    self.assertEquals(account['year'], '2012')

  def test_mary_index(self):
    response = self.run_get('mary', '/api/budget')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)
    account = result[0]
    self.assertEquals(account['name'], 'Victoria')
    self.assertEquals(account['year'], '2011')

  def test_unauthorized(self):
    response = self.run_get('mary', '/api/budget/30')
    self.assertEquals(response.status_code, 404)

    response = self.run_get('fred', '/api/budget/33')
    self.assertEquals(response.status_code, 404)

  def test_one(self):
    response = self.run_get('fred', '/api/budget/31')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(result['name'], 'Maggot')
    self.assertEquals(result['year'], '2011')


class BudgetCreateTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_budget']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/budget')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'name': 'Reelingpit',
        'year': 2013 })
    response = self.run_post(
        'fred',
        '/api/budget',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)
    budget_id = result['id']

    response = self.run_get('fred', '/api/budget/%s' % budget_id)
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'Reelingpit')


class BudgetDeleteTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_budget']

  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/budget/1066')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/budget/33')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/budget/31')
    self.assertEquals(response.status_code, 200)

    response = self.run_delete('fred', '/api/budget/31')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/budget/31')
    self.assertEquals(response.status_code, 404)
