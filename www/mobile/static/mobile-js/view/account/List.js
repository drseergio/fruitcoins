MoneypitMobile.views.AccountList = Ext.extend(Ext.List, {
  store: 'Account',
  itemTpl: '{name} <div style="float:right">{balance} {currency}</div>'
});
Ext.reg('accounts', MoneypitMobile.views.AccountList);
