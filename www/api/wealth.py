# -*- coding: utf-8 -*-
from core.models import Account
from core.models import Wealth
from django.db.models import Q
from fx import get_rate
from piston.handler import BaseHandler
from piston.utils import rc


class WealthHandler(BaseHandler):
  model = Wealth

  def read(self, request):
    wealth = request.session['wealth']
    accounts = Account.objects.filter(wealth=wealth)

    balance = 0
    deposits = 0
    withdrawals = 0

    for account in accounts:
      if account.currency != wealth.currency:
        rate = get_rate(
            account.currency.symbol,
            wealth.currency.symbol)
        balance += account.balance * rate
        deposits += account.total_deposits * rate
        withdrawals += account.total_withdrawals * rate
      else:
        balance += account.balance
        deposits += account.total_deposits
        withdrawals += account.total_withdrawals

    return {
        'balance' : balance,
        'currency': wealth.currency.symbol,
        'income'  : deposits,
        'expense' : withdrawals }
