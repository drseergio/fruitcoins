Ext.define('moneypit.store.NetWorth', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.NetWorth',

  proxy      : {
    type: 'rest',
    url : '/api/report/networth',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  remoteGroup: true,
  remoteSort : true
});
