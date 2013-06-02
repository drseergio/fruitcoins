# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class UserTest(ApiTestCase):
  fixtures = ['user_fred']

  def test_auth_required(self):
    self.auth_required(['user/currency', 'user/change'])
