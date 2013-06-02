# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class AccountEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['account', 'account/331', 'account/search'])

  def test_index_empty(self):
    response = self.run_get('fred', '/api/account')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

  def test_empty_account(self):
    response = self.run_get('fred', '/api/account/55')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('fred', '/api/account/*(&$@*&(')
    self.assertEquals(response.status_code, 404)

  def test_empty_search(self):
    response = self.run_get('fred', '/api/account/search')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')

    response = self.run_get('fred', '/api/account/search?query=@*&(#(*&*(@E!')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '[]')


class AccountReadTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_account']

  def test_fred_index(self):
    response = self.run_get('fred', '/api/account')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)
    account = result[0]
    self.assertEquals(account['balance'], '0')
    self.assertEquals(account['name'], 'UBS checking')
    self.assertEquals(account['type'], 2)
    self.assertEquals(account['id'], 1000)
    self.assertEquals(account['currency'], 'CHF')

  def test_mary_index(self):
    response = self.run_get('mary', '/api/account')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 1)
    account = result[0]
    self.assertEquals(account['balance'], '0')
    self.assertEquals(account['name'], 'RBS saving')
    self.assertEquals(account['type'], 1)
    self.assertEquals(account['id'], 1001)
    self.assertEquals(account['currency'], 'EUR')


class AccountReadTestMany(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_account_many']

  def test_account_order(self):
    response = self.run_get('fred', '/api/account')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(result), 5)
    self.assertEquals(result[0]['id'], 1000)
    self.assertEquals(result[1]['id'], 1001)
    self.assertEquals(result[2]['id'], 1002)
    self.assertEquals(result[3]['id'], 1004)
    self.assertEquals(result[4]['id'], 1003)

  def test_unauthorized(self):
    response = self.run_get('fred', '/api/account/1005')
    self.assertEquals(response.status_code, 404)
    response = self.run_get('mary', '/api/account/1005')
    self.assertEquals(response.status_code, 200)

  def test_success(self):
    response = self.run_get('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'UBS checking')
    self.assertEquals(result['currency'], 'CHF')
    self.assertEquals(result['opened_date'], '2008-01-01')
    self.assertEquals(result['balance'], '0')
    self.assertEquals(result['type'], 2)
    self.assertEquals(result['id'], 1000)

  def test_search(self):
    response = self.run_get('fred', '/api/account/search?query=uBS')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(len(result), 2)


class AccountAddTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_account_many']

  def test_no_arguments(self):
    response = self.run_post('fred', '/api/account')
    self.assertEquals(response.status_code, 400)

  def test_success(self):
    data = simplejson.dumps({
        'name': 'New World Order',
        'opened_date': '1/1/1970',
        'opening_balance': 100,
        'type': 1,
        'currency': 1 })
    response = self.run_post(
        'fred',
        '/api/account',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)
    account_id = result['id']

    response = self.run_get('fred', '/api/account/%s' % account_id)
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'New World Order')
    self.assertEquals(result['currency'], 'CHF')
    self.assertEquals(result['opened_date'], '1970-01-01')
    self.assertEquals(result['balance'], '100')
    self.assertEquals(result['type'], 1)
    self.assertEquals(result['id'], 1006)

    response = self.run_get('fred', '/api/wealth')
    result = simplejson.loads(response.content)
    self.assertEquals(result['balance'], '100')


class AccountUpdateTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_account_many']

  def test_no_arguments(self):
    response = self.run_put('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 400)

  def test_unauthorized(self):
    data = simplejson.dumps({'name': 'workamongous'})
    response = self.run_put(
        'fred',
        '/api/account/1006',
        data,
        content_type='application/json')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    data = simplejson.dumps({
        'name': 'New World Order' })
    response = self.run_put(
        'fred',
        '/api/account/1000',
        data=data,
        content_type='application/json')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['success'], True)

    response = self.run_get('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 200)
    result = simplejson.loads(response.content)
    self.assertEquals(result['name'], 'New World Order')


class AccountDeleteTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary', 'api_account_many']
   
  def test_no_arguments(self):
    response = self.run_delete('fred', '/api/account/1066')
    self.assertEquals(response.status_code, 404)

  def test_unauthorized(self):
    response = self.run_delete('fred', '/api/account/1006')
    self.assertEquals(response.status_code, 404)

  def test_success(self):
    response = self.run_get('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 200)

    response = self.run_delete('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 200)

    response = self.run_get('fred', '/api/account/1000')
    self.assertEquals(response.status_code, 404)
