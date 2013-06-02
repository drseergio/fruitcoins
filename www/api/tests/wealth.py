# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class WealthEmptyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['wealth'])


class AccountReadTest(ApiTestCase):
  fixtures = ['user_fred', 'user_mary']

  def test_fred(self):
    response = self.run_get('fred', '/api/wealth')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(result['currency'], 'CHF')

  def test_mary(self):
    response = self.run_get('mary', '/api/wealth')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(result['currency'], 'EUR')
