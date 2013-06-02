# -*- coding: utf-8 -*-
from api import get_json_response
from fx.models import Currency


def index(request):
  currencies = Currency.objects.all().order_by('symbol')
  return get_json_response(currencies, _json_currency_handler)


def _json_currency_handler(currency):
  return {
      'id': currency.id,
      'symbol': currency.symbol,
      'name': '%s (%s)' % (currency.symbol, currency.name)}
