Ext.define('moneypit.store.AccountType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text' : 'Saving',
      'value': 1
    }, {
      'text' : 'Checking',
      'value': 2
    }, {
      'text' : 'Cash',
      'value': 3
    }, {
      'text' : 'Credit Card',
      'value': 4
    }, {
      'text' : 'Generic asset',
      'value': 6
  }]
});
