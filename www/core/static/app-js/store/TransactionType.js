Ext.define('moneypit.store.TransactionType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text'  : 'Withdrawal',
      'value': 1
    }, {
      'text'  : 'Deposit',
      'value': 2
    }, {
      'text'  : 'Transfer',
      'value': 3
  }]
});
