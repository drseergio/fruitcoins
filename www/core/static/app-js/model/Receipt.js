Ext.define('moneypit.model.Receipt', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      'id',
      'date' ],

  proxy         : {
    type: 'rest',
    url : '/api/receipt'
  },
});
