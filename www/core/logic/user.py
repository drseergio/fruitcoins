# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from core.models import Category
from core.models import Wealth
from fx.models import Currency
from logging import getLogger

logger = getLogger('core')


def wealth_exists(request):
  user = request.user
  logger.debug('Checking if user account %s exists.', user)
  try:
    request.session['wealth'] = Wealth.objects.get(user=user)
    return True
  except ObjectDoesNotExist:
    logger.info('Wealth does not exist %s.', user)
    return False


def create_default_categories(wealth):
  logger.debug('Creating default categories')
  salary = _create_category(wealth, 'Salary', Category.TYPE_INCOME)
  _create_category(wealth, 'Gifts received', Category.TYPE_INCOME)
  _create_category(wealth, 'Bonus', Category.TYPE_INCOME, salary)
  _create_category(wealth, 'Interest', Category.TYPE_INCOME)
  _create_category(wealth, 'Dividends', Category.TYPE_INCOME)
  auto = _create_category(wealth, 'Auto & Transport', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Gasoline', Category.TYPE_EXPENSE, parent=auto)
  _create_category(wealth, 'Insurance', Category.TYPE_EXPENSE, parent=auto)
  _create_category(wealth, 'Service', Category.TYPE_EXPENSE, parent=auto)
  utilities = _create_category(wealth, 'Utilities', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Electricity', Category.TYPE_EXPENSE, parent=utilities)
  _create_category(wealth, 'Internet', Category.TYPE_EXPENSE, parent=utilities)
  _create_category(wealth, 'Cell phone', Category.TYPE_EXPENSE, parent=utilities)
  _create_category(wealth, 'Heating', Category.TYPE_EXPENSE, parent=utilities)
  _create_category(wealth, 'Water', Category.TYPE_EXPENSE, parent=utilities)
  _create_category(wealth, 'Cable', Category.TYPE_EXPENSE, parent=utilities)
  education = _create_category(wealth, 'Education', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Books', Category.TYPE_EXPENSE, parent=education)
  _create_category(wealth, 'Tuition', Category.TYPE_EXPENSE, parent=education)
  entertainment = _create_category(wealth, 'Entertainment', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Books', Category.TYPE_EXPENSE, parent=entertainment)
  _create_category(wealth, 'Subscriptions', Category.TYPE_EXPENSE, parent=entertainment)
  _create_category(wealth, 'Movies & music', Category.TYPE_EXPENSE, parent=entertainment)
  _create_category(wealth, 'Concerts', Category.TYPE_EXPENSE, parent=entertainment)
  charges = _create_category(wealth, 'Charges', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Bank fee', Category.TYPE_EXPENSE, parent=charges)
  _create_category(wealth, 'Transfer fee', Category.TYPE_EXPENSE, parent=charges)
  _create_category(wealth, 'ATM fee', Category.TYPE_EXPENSE, parent=charges)
  food = _create_category(wealth, 'Food', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Groceries', Category.TYPE_EXPENSE, parent=food)
  _create_category(wealth, 'Restaurants', Category.TYPE_EXPENSE, parent=food)
  _create_category(wealth, 'Coffee shops', Category.TYPE_EXPENSE, parent=food)
  _create_category(wealth, 'Gifts & donations', Category.TYPE_EXPENSE)
  health = _create_category(wealth, 'Healthcare', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Sports', Category.TYPE_EXPENSE, parent=health)
  _create_category(wealth, 'Gym', Category.TYPE_EXPENSE, parent=health)
  _create_category(wealth, 'Spa', Category.TYPE_EXPENSE, parent=health)
  _create_category(wealth, 'Doctors', Category.TYPE_EXPENSE, parent=health)
  _create_category(wealth, 'Insurance', Category.TYPE_EXPENSE, parent=health)
  home = _create_category(wealth, 'Home', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Rent', Category.TYPE_EXPENSE, parent=home)
  _create_category(wealth, 'Furnishings', Category.TYPE_EXPENSE, parent=home)
  _create_category(wealth, 'Insurance', Category.TYPE_EXPENSE, parent=home)
  personal = _create_category(wealth, 'Personal', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Haircut', Category.TYPE_EXPENSE, parent=personal)
  _create_category(wealth, 'Massage', Category.TYPE_EXPENSE, parent=personal)
  possessions = _create_category(wealth, 'Possessions', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Electronics', Category.TYPE_EXPENSE, parent=possessions)
  _create_category(wealth, 'Clothing & accessories', Category.TYPE_EXPENSE, parent=possessions)
  _create_category(wealth, 'Sport goods', Category.TYPE_EXPENSE, parent=possessions)
  travel = _create_category(wealth, 'Travel', Category.TYPE_EXPENSE)
  _create_category(wealth, 'Vacation', Category.TYPE_EXPENSE, parent=travel)
  _create_category(wealth, 'Hotel', Category.TYPE_EXPENSE, parent=travel)
  _create_category(wealth, 'Transport', Category.TYPE_EXPENSE, parent=travel)


def _create_category(wealth, name, type, parent=None):
  category = Category(
      wealth=wealth,
      name=name,
      parent=parent,
      total_balance=0,
      balance=0,
      type=type)
  category.save()
  return category
