Ext.regStore('NetWorth', {
  model: 'NetWorth',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/report/networth',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
