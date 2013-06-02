Ext.regModel('Transaction', {
  fields: [
    {name: 'id', type: 'int'},
    {name: 'type', type: 'int'},
    {name: 'amount', type: 'float'},
    {name: 'amount_real', type: 'float'},
    {name: 'description', type: 'string'},
    {name: 'category', type: 'string'},
    {name: 'date', type: 'date'}
  ]
});
