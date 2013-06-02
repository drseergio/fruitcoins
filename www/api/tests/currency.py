# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class CurrencyTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_success(self):
    response = self.run_get('fred', '/api/fx/index')
    result = simplejson.loads(response.content)
    self.assertEquals(response.status_code, 200)
    self.assertTrue(len(result['items']) > 100)
