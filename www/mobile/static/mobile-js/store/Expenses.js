Ext.regStore('Expenses', {
  model: 'Expenses',

  proxy: {
    type: 'rest',
    url : '/api/report/expenses',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
