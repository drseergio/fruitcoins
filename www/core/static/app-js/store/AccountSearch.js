Ext.define('moneypit.store.AccountSearch', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.AccountSearch',
  autoLoad   : true,

  proxy      : {
    type: 'rest',
    url : '/api/account/search'
  },
  remoteSort : true
});
