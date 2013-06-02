Ext.define('moneypit.model.BudgetLine', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      'id',
      { name: 'amount', type: 'float' },
      { name: 'total_amount', type: 'float' },
      'period',
      'category',
      { name: 'balance', type: 'float' },
      { name: 'progress', type: 'int' },
      { name: 'category_id', type: 'int'},
      { name: 'type', type: 'int'} ],

  proxy         : {
    type: 'rest',
    url : '/api/budgetline'
  },
});
