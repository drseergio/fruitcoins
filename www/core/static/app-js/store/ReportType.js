Ext.define('moneypit.store.ReportType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text' : 'Net worth monthly',
      'value': 1
    }, {
      'text' : 'NetIncome monthly',
      'value': 4
    }, {
      'text' : 'Expenses monthly',
      'value': 2
    }, {
      'text' : 'Incomes monthly',
      'value': 3
    }, {
      'text' : 'Expense breakdown',
      'value': 5
    }, {
      'text' : 'Income breakdown',
      'value': 6
  }]
});
