Ext.regStore('Account', {
  model: 'Account',
 
  proxy: {
    type: 'rest',
    url : '/api/account',
  },
});
