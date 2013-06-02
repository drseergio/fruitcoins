Ext.define('moneypit.store.Tag', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Tag',
  autoLoad   : true,
  autoSync   : true,

  proxy      : {
    type: 'rest',
    url : '/api/tag'
  },
  remoteSort : true
});
