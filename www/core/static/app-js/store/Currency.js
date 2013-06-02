Ext.define('moneypit.store.Currency', {
  extend  : 'Ext.data.Store',
  model   : 'moneypit.model.Currency',
  autoLoad: true,

  proxy   : {
    type  : 'ajax',
    url   : '/api/fx/index',
    reader: {
      root         : 'items',
      totalProperty: 'count'
    }
  }
});
