# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class BudgetLineEmptyTest(ApiTestCase):
  fixtures = ['user_fred', 'api_budget']

  def test_auth_required(self):
    self.auth_required(['budgetline', 'budgetline/331'])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/budgetline', {'budget': 30})
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

  def test_empty_account(self):
    response = self.run_get('fred', '/api/budgetline/55', {'budget': 30})
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/budgetline/@$!@^&', {'budget': 30})
    self.assertEquals(response.status_code, 404)


class BudgetLineReadTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_budget',
      'api_category',
      'api_budgetline']

  def test_fred_index(self):
    response = self.run_get('fred', '/api/budgetline', {'budget': 31})
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 3)
    self.assertEquals(result[0]['total_amount'], '520')

  def test_mary_index(self):
    response = self.run_get('mary', '/api/budgetline', {'budget': 33})
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)
    self.assertEquals(result[0]['total_amount'], '200')


class BudgetLineCreateTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_budget',
      'api_category',
      'api_budgetline']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/budgetline')
    self.assertEquals(response.status_code, 400)
    response = self.run_post('fred', '/api/budgetline', {'budget': 31})
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'period': 1,
        'amount': 100,
        'budget': 30,
        'category_id': 2002 })
    response = self.run_post(
        'fred',
        '/api/budgetline?budget=30',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)
    line_id = result['id'] 

    response = self.run_get(
        'fred',
        '/api/budgetline/%s' % line_id,
        {'budget': 30})
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['total_amount'], '5200')


class BudgetLineDeleteTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_budget',
      'api_category',
      'api_budgetline']

  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/budgetline/788?budget=30')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/budgetline/53?budget=33')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/budgetline/51?budget=31')
    self.assertEquals(response.status_code, 200)

    response = self.run_delete('fred', '/api/budgetline/51?budget=31')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/budgetline/51?budget=31')
    self.assertEquals(response.status_code, 404)


class BudgetLineUpdateTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_budget',
      'api_category',
      'api_budgetline']

  def test_no_arguments(self):
    response = self.run_put('fred', '/api/budgetline/51?budget=31')
    self.assertEquals(response.status_code, 400)

  def test_unauthorized(self):
    response = self.run_put('fred', '/api/budgetline/53?budget=33')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'period': 1,
        'amount': 12,
        'category_id': 2003 })
    response = self.run_put(
        'fred',
        '/api/budgetline/52?budget=31',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/budgetline/52?budget=31')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['total_amount'], '624')
