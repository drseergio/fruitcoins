Ext.regStore('ExpenseBreakdown', {
  model: 'ExpenseBreakdown',

  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/report/category/expense',
    reader       : {
      type         : 'json',
      root         : 'items'
    }
  },
});
