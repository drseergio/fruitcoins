# -*- coding: utf-8 -*-
from core.models import Budget
from core.models import BudgetLine


def delete_budget(budget):
  lines = BudgetLine.objects.filter(budget=budget)
  for line in lines:
    line.delete()
  budget.delete()
