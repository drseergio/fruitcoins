Ext.define('moneypit.store.Transaction', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Transaction',

  proxy      : {
    type  : 'rest',
    url   : '/api/transaction/wealth',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  groupField : 'period',
  remoteGroup: true,
  remoteSort : true
});
