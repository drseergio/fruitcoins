MoneypitMobile.views.AccountList = Ext.extend(Ext.List, {
  store: 'Account',
  emptyText: 'No accounts :(, create some at fruitcoins.com using a desktop browser',
  itemTpl: '{name} <div style="float:right">{balance} {currency}</div>'
});
Ext.reg('accounts', MoneypitMobile.views.AccountList);
