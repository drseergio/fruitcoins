Ext.define('moneypit.store.IncomeBreakdown', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.IncomeBreakdown',
  sorters    : [{
      property : 'full_name',
      direction: 'ASC'
    }, {
      property : 'amount',
      direction: 'ASC'
  }],

  proxy      : {
    type: 'rest',
    url : '/api/report/category/income',
    reader: {
      type : 'json',
      root : 'items',
    }
  },
});
