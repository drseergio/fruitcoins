# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class LiberationTest(ApiTestCase):
  def test_auth_required(self):
    self.auth_required([
        'liberation/export/kmy',
        'liberation/preview',
        'liberation/commit',
        'liberation/discard',
        'liberation/progress',
        'liberation/upload' ])
