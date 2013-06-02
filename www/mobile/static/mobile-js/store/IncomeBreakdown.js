Ext.regStore('IncomeBreakdown', {
  model: 'IncomeBreakdown',

  proxy: {
    type: 'rest',
    url : '/api/report/category/income',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
