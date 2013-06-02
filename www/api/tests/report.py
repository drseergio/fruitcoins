# -*- coding: utf-8 -*-
from api import ApiTestCase
from django.utils import simplejson


class ReportTest(ApiTestCase):
  def test_auth_required(self):
    self.auth_required([
        'report/category/income',
        'report/category/expense',
        'report/netincome',
        'report/networth',
        'report/expenses',
        'report/incomes'])
