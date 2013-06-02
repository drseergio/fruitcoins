Ext.define('moneypit.store.Receipt', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Receipt',
  autoLoad   : true,

  proxy      : {
    type: 'rest',
    url : '/api/receipt'
  },
  remoteSort : true
});
