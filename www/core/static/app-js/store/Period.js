Ext.define('moneypit.store.Period', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text'  : 'Weekly',
      'value': 1
    }, {
      'text'  : 'Monthly',
      'value': 2
    }, {
      'text'  : 'Quarterly',
      'value': 3
    }, {
      'text'  : 'Yearly',
      'value': 4
    }]
});
