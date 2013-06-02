MoneypitMobile.views.Login = Ext.extend(Ext.form.FormPanel, {
  scroll        : 'vertical',
  url           : fruitcoinsUrl + 'api/user/login',
  fullscreen    : true,
  standardSubmit: false,

  items         : [{
    xtype       : 'fieldset',
    title       : 'Login to fruitcoins.com',
    instructions: 'You may also use Google, LinkedIn or Facebook to sign-in. An account must be created on a desktop web-browser first. Registration on mobile version is not available.',
    defaults    : {
      required  : true,
      labelAlign: 'left',
      labelWidth: '45%'
    },
    items       : [{
        xtype       : 'textfield',
        name        : 'username',
        label       : 'Username',
        useClearIcon: true
      }, {
        xtype       : 'passwordfield',
        name        : 'password',
        label       : 'Password',
        useClearIcon: false
      }]
    }],
    dockedItems   : [{
      xtype: 'toolbar',
      dock: 'bottom',
      items: [{
          id: 'social-login-google',
          text: 'Google',
        }, {
          id: 'social-login-linkedin',
          text: 'LinkedIn',
        }, {
          id: 'social-login-facebook',
          text: 'Facebook',
        }, {
          xtype: 'spacer',
        }, {
          id: 'login-button',
          text: 'Login',
          ui: 'confirm',
      }]
    }]
});
Ext.reg('login', MoneypitMobile.views.Login);
