Ext.define('moneypit.store.Account', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Account',
  autoLoad   : true,
  autoSync   : true,

  proxy      : {
    type: 'rest',
    url : '/api/account'
  },
  remoteSort : true
});
