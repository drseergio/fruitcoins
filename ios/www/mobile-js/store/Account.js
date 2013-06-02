Ext.regStore('Account', {
  model: 'Account',
 
  proxy: {
    type: 'rest',
    url : fruitcoinsUrl + 'api/account',
  },
});
