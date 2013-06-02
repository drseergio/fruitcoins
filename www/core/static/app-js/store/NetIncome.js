Ext.define('moneypit.store.NetIncome', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.NetIncome',

  proxy      : {
    type: 'rest',
    url : '/api/report/netincome',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  remoteGroup: true,
  remoteSort : true
});
