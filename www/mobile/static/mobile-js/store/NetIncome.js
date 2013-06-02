Ext.regStore('NetIncome', {
  model: 'NetIncome',

  proxy: {
    type: 'rest',
    url : '/api/report/netincome',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
