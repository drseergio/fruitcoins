# -*- coding: utf-8 -*-
from core.models import Account
from core.models import Wealth
from fx import refresh_rates


def check_rates(orig_func):
  def check(*args, **kwargs):
    request = args[0]
    if not request.user.is_anonymous():
      wealth = Wealth.objects.get(user=request.user)
      currencies = []
      accounts = Account.objects.filter(wealth=wealth)
      for account in accounts:
        currencies.append(account.currency.symbol)
      refresh_rates(list(set(currencies)))
    return orig_func(*args, **kwargs)
  return check
