Ext.regStore('NetIncome', {
  model: 'NetIncome',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/report/netincome',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
