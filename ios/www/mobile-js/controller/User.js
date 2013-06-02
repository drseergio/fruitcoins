Ext.regController('User', {
  systems: [
    '#social-login-google',
    '#social-login-linkedin',
    '#social-login-facebook'
  ],

  logout: function() {
    Ext.Msg.confirm("Confirmation",
      "Are you sure want to logout?",
      function(btn) {
        if (btn == "yes") {
          CookiePlugin.nativeFunction();
          var viewport = MoneypitMobile.viewport;
          var tabbar = Ext.getCmp('tab-bar-mvc');
          tabbar.hide();
          viewport.componentLayout.childrenChanged = true;
          viewport.doComponentLayout();
          Ext.dispatch({
            controller: 'User',
            action: 'login'
          });
        }
    });
  },

  login: function() {
    if (!this.loginView) {
      this.loginView = this.render({
        xtype: 'login',
      });
      var loginBtn = this.loginView.query('#login-button')[0];
      loginBtn.setHandler(function() {
        this.loginHandler(this.loginView);
      }, this);
      var me = this;
      this.systems.forEach(function(item) {
        me.loginView.query(item)[0].setHandler(function() {
          me.socialHandler(item);
        });
      });
    }

    this.application.viewport.setActiveItem(this.loginView);
  },

  socialHandler: function(id) {
    var system = id.split("-").pop();
    //location.href = fruitcoinsUrl + 'login/' + system;
    var me = this;
    BrowserPlugin.onLocationChange = function(loc){ me.socialLocChange(loc); };
    window.plugins.childBrowser.showWebPage(fruitcoinsUrl + 'login/' + system);
  },

  socialLocChange: function(loc) {
    var me = this;
    if (loc.indexOf('https://fruitcoins.com/mobile/user/login') == 0) {
      window.plugins.childBrowser.close();
    }
    if (loc.indexOf('https://fruitcoins.com/mobile') == 0) {
      window.plugins.childBrowser.close();
      me.openMainScreen();
    }
  },

  loginHandler: function(form) {
    var me = this;
    form.submit({
      method: 'post',
      waitMsg: {
        message: 'Logging you in'
      },
      success: function() {
        form.reset();
        me.openMainScreen();
      }
    });
  },

  openMainScreen: function() {
    var viewport = MoneypitMobile.viewport;
    var tabbar = Ext.getCmp('tab-bar-mvc');
    tabbar.show();
    viewport.componentLayout.childrenChanged = true;
    viewport.doComponentLayout();
    Ext.dispatch({
      controller: 'Account',
      action: 'index'
    });
  }
});
