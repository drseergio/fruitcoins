Ext.define('moneypit.view.category.Edit', {
    extend: 'Ext.window.Window',
    alias : 'widget.categoryedit',

    title : 'Category',
    layout: 'fit',
    autoShow: true,
    modal   : true,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        border: false,
        frame: true,
        items: [{
            xtype: 'textfield',
            id: 'category-name',
            name : 'text',
            allowBlank: false,
            hideLabel: true,
            emptyText: 'Category name'
          }, {
            xtype: 'textfield',
            id: 'category-description',
            name : 'description',
            hideLabel: true,
            emptyText: 'Description'
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
