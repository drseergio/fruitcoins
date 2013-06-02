# -*- coding: utf-8 -*-
from api import MoneypitResource as Resource
from api.account import AccountHandler
from api.budget import BudgetHandler
from api.budgetline import BudgetLineHandler
from api.category import CategoryHandler
from api.liberation import ImportHandler
from api.receipt import ReceiptHandler
from api.tag import TagHandler
from api.transaction import TransactionHandler
from api import DjangoAuthentication
from api.wealth import WealthHandler
from django.conf.urls.defaults import patterns


auth = DjangoAuthentication()
account_resource = Resource(AccountHandler, authentication=auth)
budget_resource = Resource(BudgetHandler, authentication=auth)
budgetline_resource = Resource(BudgetLineHandler, authentication=auth)
category_resource = Resource(CategoryHandler, authentication=auth)
import_resource = Resource(ImportHandler, authentication=auth)
receipt_resource = Resource(ReceiptHandler, authentication=auth)
tag_resource = Resource(TagHandler, authentication=auth)
transaction_resource = Resource(TransactionHandler, authentication=auth)
wealth_resource = Resource(WealthHandler, authentication=auth)

urlpatterns = patterns(
  'api.currency',
  (r'^fx/index', 'index'))

urlpatterns += patterns('',
  (r'^account/(?P<account_id>\d+)$', account_resource),
  (r'^account/(?P<search>search)$', account_resource),
  (r'^account$', account_resource))

urlpatterns += patterns('',
  (r'^budget/(?P<budget_id>\d+)$', budget_resource),
  (r'^budget$', budget_resource))

urlpatterns += patterns('',
  (r'^budgetline/(?P<budgetline_id>\d+)$', budgetline_resource),
  (r'^budgetline$', budgetline_resource))

urlpatterns += patterns('',
  (r'^category/move$', 'api.category.move'),
  (r'^category/(?P<category_id>\d+)$', category_resource),
  (r'^category/(?P<search>search)$', category_resource),
  (r'^category$', category_resource))


urlpatterns += patterns('api.feedback',
  (r'^feedback$', 'feedback'))

urlpatterns += patterns('',
  (r'^tag/(?P<tag_id>\d+)$', tag_resource),
  (r'^tag$', tag_resource))

urlpatterns += patterns('',
  (r'^liberation/export/kmy$', 'api.liberation.export_kmy'),
  (r'^liberation/preview$', import_resource),
  (r'^liberation/commit$', 'api.liberation.commit'),
  (r'^liberation/discard$', 'api.liberation.discard'),
  (r'^liberation/progress$', 'api.liberation.progress'),
  (r'^liberation/upload$', 'api.liberation.upload'))

urlpatterns += patterns('',
  (r'^receipt/(?P<receipt_id>\d+)$', receipt_resource),
  (r'^receipt$', receipt_resource),
  (r'^receipt/image$', 'api.receipt.image'),
  (r'^receipt/upload$', 'api.receipt.upload'))

urlpatterns += patterns('',
  (r'^report/expenses$', 'api.report.expenses'),
  (r'^report/incomes$', 'api.report.incomes'),
  (r'^report/netincome', 'api.report.netincome'),
  (r'^report/category/(?P<category_type>(income|expense))$', 'api.report.categories'),
  (r'^report/networth$', 'api.report.networth'))

urlpatterns += patterns('',
  (r'^transaction$', transaction_resource),
  (r'^transaction/csv$', 'api.transaction.csv'),
  (r'^transaction/upload/(?P<account_id>\d+)$', 'api.transaction.upload'),
  (r'^transaction/associate$', 'api.transaction.tag'),
  (r'^transaction/deassociate$', 'api.transaction.remove_tags'),
  (r'^transaction/(?P<transaction_type>(account|category|tag|wealth))/(?P<object_id>\d+)$', transaction_resource),
  (r'^transaction/(?P<transaction_type>(account|category|tag|wealth))$', transaction_resource))

urlpatterns += patterns(
  'api.user',
  (r'^user/invite$', 'invite'),
  (r'^user/currency$', 'currency'),
  (r'^user/change$', 'change'),
  (r'^user/reset$', 'reset'),
  (r'^user/resetpassword$', 'reset_password'),
  (r'^user/login$', 'login'),
  (r'^user/register$', 'register'))

urlpatterns += patterns('',
  (r'^wealth$', wealth_resource))
