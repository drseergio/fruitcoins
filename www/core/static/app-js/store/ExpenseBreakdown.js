Ext.define('moneypit.store.ExpenseBreakdown', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.ExpenseBreakdown',
  sorters    : [{
      property : 'full_name',
      direction: 'ASC'
    }, {
      property : 'amount',
      direction: 'ASC'
  }],

  proxy      : {
    type: 'rest',
    url : '/api/report/category/expense',
    reader: {
      type : 'json',
      root : 'items',
    }
  },
});
