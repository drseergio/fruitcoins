Ext.define('moneypit.store.Category', {
  extend     : 'Ext.data.TreeStore',
  model      : 'moneypit.model.Category',
  autoLoad   : true,
  autoSync   : true,

  proxy      : {
    type: 'rest',
    url : '/api/category'
  },
  remoteSort : true
});
