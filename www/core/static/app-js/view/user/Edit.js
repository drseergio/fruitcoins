Ext.define('moneypit.view.user.Edit', {
    extend: 'Ext.window.Window',
    alias : 'widget.useredit',

    title : 'Modify my account',
    layout: 'fit',
    autoShow: true,
    width   : 320,
    modal   : true,
    border  : false,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        url  : '/api/user/change',
        frame: true,
        items: [{
            id        : 'edit-email',
            xtype     : 'textfield',
            vtype     : 'email',
            fieldLabel: 'e-mail',
            name      : 'email',
            labelAlign: 'right',
            labelSeparator: '',
           }, {
            id        : 'old-password',
            xtype     : 'textfield',
            fieldLabel: 'current password',
            inputType : 'password',
            name      : 'old_password',
            labelSeparator: '',
            labelAlign: 'right',
            allowBlank: false
          }, {
            id        : 'edit-password',
            xtype     : 'textfield',
            fieldLabel: 'new password',
            inputType : 'password',
            name      : 'new_password1',
            labelSeparator: '',
            labelAlign: 'right',
          }, {
            xtype     : 'textfield',
            fieldLabel: 'repeat',
            inputType : 'password',
            name      : 'new_password2',
            labelSeparator: '',
            labelAlign: 'right',
            validator : function(value) {
              var password1 = this.previousSibling('[name=new_password1]');
              return (value === password1.getValue()) ? true : 'Passwords do not match.'
            }
        }]
      }];

      this.buttons = [{
          text: 'Save',
          action: 'save',
          disabled: true
        }, {
          text: 'Cancel',
          scope: this,
          handler: this.close
      }];

      this.callParent(arguments);
    }
});
