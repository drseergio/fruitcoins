Ext.define('moneypit.controller.User', {
  extend          : 'Ext.app.Controller',
  views           : [ 'user.Edit', 'feedback.Add' ],
  stores          : [ ],
  models          : [ ],

  refs: [{
      selector: 'useredit',
      ref     : 'userEdit'
    }, {
      selector: 'feedback',
      ref     : 'feedbackAdd'
  }],

  init            : function() {
    this.control({
      'useredit button[action=save]' : {
        click: this.saveUser
      },
      'useredit #edit-email'         : {
        afterrender: this.setFocus,
        change: this.toggleSave
      },
      'useredit #edit-password'      : {
        change: this.toggleSave
      },
      'feedback #feedback-field'     : {
        afterrender: this.setFocus,
      },
      'feedback button[action=send]' : {
        click: this.sendFeedback
      },
    });
    this.application.on({
      scope            : this
    });
    if (Ext.get('account')) {
      Ext.get('account').on('click', function() {
        Ext.widget('useredit');
      });
    }
    Ext.get('tellus').on('click', function() {
      Ext.widget('feedback');
    });
  },

  setFocus: function(field) {
    field.focus(false, 400);
  },

  toggleSave: function() {
    var win = this.getUserEdit();
    var form = win.down('form');

    var email = form.down('#edit-email').getValue();
    var password = form.down('#edit-password').getValue();

    if (email || password) {
      win.down('button[action=save]').enable();
    } else {
      win.down('button[action=save]').disable();
    }
  },

  saveUser: function() {
    var win = this.getUserEdit();
    var form = win.down('form');

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      form.submit({
        success: function(rec, op) {
          win.close();
        },
        failure: function(rec, op) {
          form.el.unmask();
          var errors = op.result.errors;
          form.getForm().markInvalid(errors);
        },
      });
    }
  },

  sendFeedback: function() {
    var win = this.getFeedbackAdd();
    var form = win.down('form');

    if (form.getForm().isValid()) {
      form.el.mask('Thank you! Sending..');
      form.submit({
        success: function(rec, op) {
          win.close();
        },
        failure: function(rec, op) {
          win.close();
        },
      });
    }
  }
});
