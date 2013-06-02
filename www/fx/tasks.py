# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from celery.decorators import task
from celery.registry import tasks
from core.errors import MoneypitException
from fx.models import CurrencyRate
from logging import getLogger
from settings import CURRENCY_RATE_VALIDITY
from settings import RATE_URL
from urllib2 import urlopen
from urllib2 import URLError

logger = getLogger('fx')


@task()
def fetch_rate(symbol_from, symbol_to):
  logger.info('Requesting currency rate from %s to %s ',
               symbol_from, symbol_to)
  try:
    ratehandler = urlopen(RATE_URL % (symbol_from, symbol_to))
    new_rate = Decimal(ratehandler.read().rstrip())
    ratehandler.close()

    cache.set(
        '%s%s' % (symbol_from, symbol_to),
        new_rate,
        CURRENCY_RATE_VALIDITY);

    try:
      rate = CurrencyRate.objects.get(
          source=symbol_from,
          destination=symbol_to)
    except ObjectDoesNotExist:
      rate = CurrencyRate(source=symbol_from, destination=symbol_to)

    rate.rate = new_rate
    rate.last_update = datetime.utcnow()
    rate.save()
    return new_rate
  except URLError:
    logger.error('Failed to get currency rate from %s to %s',
        symbol_from,
        symbol_to)
    raise MoneypitException('Failed to get currency')


tasks.register(fetch_rate)
