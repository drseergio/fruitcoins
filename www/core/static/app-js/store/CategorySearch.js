Ext.define('moneypit.store.CategorySearch', {
  extend     : 'Ext.data.Store',
  model      : 'moneypit.model.CategorySearch',

  proxy      : {
    type: 'rest',
    url : '/api/category/search'
  },
  sortInfo: {
    field    : 'name',
    direction: 'ASC'
  },
});
