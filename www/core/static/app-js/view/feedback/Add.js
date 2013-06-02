Ext.define('moneypit.view.feedback.Add', {
    extend: 'Ext.window.Window',
    alias : 'widget.feedback',

    title : 'Send a message to fruitcoins team',
    layout: 'fit',
    autoShow: true,
    width   : 320,
    height  : 200,
    border  : false,
    modal   : true,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        border: false,
        layout: 'fit',
        url  : '/api/feedback',
        items: [{
            id        : 'feedback-field',
            xtype     : 'textarea',
            name      : 'text',
            allowBlank: false
        }]
      }];

      this.buttons = [{
          text: 'Send',
          action: 'send'
        }, {
          text: 'Cancel',
          scope: this,
          handler: this.close
      }];

      this.callParent(arguments);
    }
});
