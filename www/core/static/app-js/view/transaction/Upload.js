Ext.define('moneypit.view.transaction.Upload', {
    extend: 'Ext.window.Window',
    alias : 'widget.upload',

    title : 'Upload transactions',
    layout: 'fit',
    autoShow: true,
    border  : false,
    modal   : true,
    width   : 200,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        border: false,
        url: '/api/transaction/upload',
        frame: true,
        items: [{
          xtype: 'filefield',
          name : 'importdata',
          allowBlank: false,
          hideLabel: true,
          anchor: '100%',
          emptyText: 'Choose file to upload..',
          buttonConfig: {
            iconCls: 'icons-browse'
          },
          buttonText: ''
        }]
      }];

      this.buttons = [{
          text: 'Upload',
          action: 'upload'
        }, {
          text: 'Cancel',
          scope: this,
          handler: this.close
      }];

      this.callParent(arguments);
    }
});
