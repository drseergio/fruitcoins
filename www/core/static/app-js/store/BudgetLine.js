Ext.define('moneypit.store.BudgetLine', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.BudgetLine',

  proxy      : {
    type: 'rest',
    url : '/api/budgetline'
  },
});
