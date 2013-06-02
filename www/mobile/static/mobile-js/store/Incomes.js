Ext.regStore('Incomes', {
  model: 'Incomes',

  proxy: {
    type: 'rest',
    url : '/api/report/incomes',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
