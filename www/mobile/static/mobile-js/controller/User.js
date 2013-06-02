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
          window.location = '/user/logout';
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
    location.href = '/login/' + system;
  },

  loginHandler: function(form) {
    form.submit({
      method: 'post',
      waitMsg: {
        message: 'Logging you in'
      },
      success: function() {
        window.location = '/mobile/';
      }
    });
  }
});
