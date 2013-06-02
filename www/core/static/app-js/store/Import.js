Ext.define('moneypit.store.Import', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.Import',
  autoLoad   : true,

  proxy      : {
    type: 'rest',
    url : '/api/liberation/preview',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  groupField : 'type',
  remoteGroup: true,
  remoteSort : true
});
