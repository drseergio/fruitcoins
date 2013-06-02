# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class TransactionEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required([
        'transaction',
        'transaction/csv',
        'transaction/upload/123',
        'transaction/associate',
        'transaction/deassociate',
        'transaction/account/123',
        'transaction/account',
        'transaction/category/123',
        'transaction/category',
        'transaction/tag/123',
        'transaction/tag',
        'transaction/wealth/123',
        'transaction/wealth' ])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/transaction/wealth?limit=25&start=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['items'], [])

  def test_empty_account(self):
    response = self.run_get('fred', '/api/transaction/account/21?limit=25&start=0')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/transaction/account/@*(&!?limit=25&start=0')
    self.assertEquals(response.status_code, 404)


class TransactionReadTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_category',
      'api_account_many',
      'api_tag',
      'api_transaction']

  def test_fred_index(self):
    response = self.run_get('fred', '/api/transaction/wealth?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '500')
    self.assertEquals(result['items'][0]['description'], 'My first salary')

    response = self.run_get('fred', '/api/transaction/account/1000?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '500')
    self.assertEquals(result['items'][0]['description'], 'My first salary')

    response = self.run_get('fred', '/api/transaction/category/2000?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '500')
    self.assertEquals(result['items'][0]['description'], 'My first salary')

  def test_mary_index(self):
    response = self.run_get('mary', '/api/transaction/wealth?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '123')
    self.assertEquals(result['items'][0]['description'], 'Donated towards New World Order')

    response = self.run_get('mary', '/api/transaction/account/1005?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '123')
    self.assertEquals(result['items'][0]['description'], 'Donated towards New World Order')

    response = self.run_get('mary', '/api/transaction/category/2005?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)
    self.assertEquals(result['items'][0]['amount'], '123')
    self.assertEquals(result['items'][0]['description'], 'Donated towards New World Order')


class TransactionAddTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_category',
      'api_account_many',
      'api_tag',
      'api_transaction']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/transaction')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'account_from': 1001,
        'category_id': 2004,
        'type': '2',
        'date': '1/1/2013',
        'amount': 17,
        'description': 'condoms' })
    response = self.run_post(
        'fred',
        '/api/transaction',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/transaction/category/2004?limit=25&start=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['items'][0]['description'], 'condoms')
    self.assertEquals(result['items'][0]['amount'], '17')


class TransactionDeleteTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_category',
      'api_account_many',
      'api_tag',
      'api_transaction']

  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/transaction/1066')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/account/81')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/transaction/account/1000?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result['items']), 1)

    response = self.run_delete('fred', '/api/transaction/wealth/80')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/transaction/account/1000?limit=25&start=0')
    result = simplejson.loads(response.content)
    self.assertEquals(len(result['items']), 0)


class TransactionUpdateTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_category',
      'api_account_many',
      'api_tag',
      'api_transaction']

  def test_no_arguments(self):
    response = self.run_put('fred', '/api/transaction/wealth/80')
    self.assertEquals(response.status_code, 400)

  def test_unauthorized(self):
    data = simplejson.dumps({'description': 'workamongous'})
    response = self.run_put(
        'fred',
        '/api/transaction/wealth/81',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    data = simplejson.dumps({
        'amount': 54,
        'type': 2,
        'category_id': 2000,
        'date': '1/1/2024',
        'description': 'New World Order' })
    response = self.run_put(
        'fred',
        '/api/transaction/wealth/80',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/transaction/account/1000?limit=25&start=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['items'][0]['description'], 'New World Order')


class TransactionTagTest(ApiTestCase):
  fixtures = [
      'user_fred',
      'user_mary',
      'api_category',
      'api_account_many',
      'api_tag',
      'api_transaction']

  def test_associate(self):
    data = simplejson.dumps({
        'associate': True,
        'tag': 70,
        'transactions': [80]})
    response = self.run_post(
        'fred',
        '/api/transaction/associate',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/transaction/tag/70?limit=25&start=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(len(result['items']), 1)

    data = simplejson.dumps({
        'associate': False,
        'tag': 70,
        'transactions': [80]})
    response = self.run_post(
        'fred',
        '/api/transaction/deassociate',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/transaction/tag/70?limit=25&start=0')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(len(result['items']), 0)
