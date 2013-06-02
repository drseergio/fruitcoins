Ext.define('moneypit.model.ExpenseBreakdown', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      { name: 'amount', type: 'float' },
      'name', 'full_name' ],
});
