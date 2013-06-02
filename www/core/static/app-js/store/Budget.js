Ext.define('moneypit.store.Budget', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Budget',
  autoLoad   : true,
  autoSync   : true,

  proxy      : {
    type: 'rest',
    url : '/api/budget'
  },
  remoteSort : true
});
