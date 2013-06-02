Ext.regStore('Transaction', {
  model: 'Transaction',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/transaction/account',
    extraParams  : {
      start: 0,
    },
    reader       : {
      type         : 'json',
      totalProperty: 'count',
      root         : 'items'
    }
  },
});
