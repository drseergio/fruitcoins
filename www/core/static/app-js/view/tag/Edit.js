Ext.define('moneypit.view.tag.Edit', {
    extend: 'Ext.window.Window',
    alias : 'widget.tagedit',

    title : 'Tag',
    layout: 'fit',
    autoShow: true,
    modal   : true,
    border  : false,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        frame: true,
        items: [{
          xtype: 'textfield',
          id   : 'tag-name',
          name : 'name',
          allowBlank: false,
          hideLabel: true,
          emptyText: 'Tag name'
        }]
      }];

      this.buttons = [{
          text: 'Save',
          action: 'save'
        }, {
          text: 'Cancel',
          scope: this,
          handler: this.close
      }];

      this.callParent(arguments);
    }
});
