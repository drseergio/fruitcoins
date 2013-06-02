Ext.regStore('NetWorth', {
  model: 'NetWorth',

  proxy: {
    type: 'rest',
    url : '/api/report/networth',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
