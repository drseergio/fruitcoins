Ext.define('moneypit.store.Expenses', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Expenses',

  proxy      : {
    type: 'rest',
    url : '/api/report/expenses',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  remoteGroup: true,
  remoteSort : true
});
