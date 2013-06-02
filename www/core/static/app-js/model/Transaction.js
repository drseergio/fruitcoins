Ext.define('moneypit.model.Transaction', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'category', type: 'string' },
      { name: 'amount', type: 'float' },
      { name: 'amount_real', type: 'float' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' },
      { name: 'description', type: 'string' },
      { name: 'type', type: 'int' },
      { name: 'period', type: 'string' },
      { name: 'account_from', type: 'int' },
      { name: 'account_id', type: 'int' },
      { name: 'category_id', type: 'int' }],

  associations: [{
      type          : 'hasMany',
      model         : 'moneypit.model.Tag',
      name          : 'tags',
    }, {
      type          : 'belongsTo',
      model         : 'moneypit.model.Category',
      associatedName: 'Category',
    }, {
      type          : 'belongsTo',
      model         : 'moneypit.model.Account',
      associatedName: 'Account',
  }],

  proxy       : {
    type: 'rest',
    url : '/api/transaction'
  }
});
