Ext.regStore('Incomes', {
  model: 'Incomes',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/report/incomes',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
