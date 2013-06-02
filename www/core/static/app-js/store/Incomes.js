Ext.define('moneypit.store.Incomes', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Incomes',

  proxy      : {
    type: 'rest',
    url : '/api/report/incomes',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  remoteGroup: true,
  remoteSort : true
});
