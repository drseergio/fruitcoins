# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class ReceiptTest(ApiTestCase):
  def test_auth_required(self):
    self.auth_required([
        'receipt/upload' ])
