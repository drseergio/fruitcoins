Ext.regStore('Expenses', {
  model: 'Expenses',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/report/expenses',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
