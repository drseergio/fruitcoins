# -*- coding: utf-8 -*-
from django.db import models


class Currency(models.Model):
  symbol = models.CharField(max_length=10)
  name = models.CharField(max_length=100, blank=True)
  code = models.CharField(max_length=10, blank=True)
  human = models.CharField(max_length=10, blank=True)
  unit = models.CharField(max_length=5)

  def __unicode__(self):
    return self.symbol


class CurrencyRate(models.Model):
  source = models.CharField(max_length=10)
  destination = models.CharField(max_length=10)
  rate = models.DecimalField(decimal_places=6, max_digits=30)
  last_update = models.DateTimeField()
