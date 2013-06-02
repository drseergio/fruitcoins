Ext.define('moneypit.view.budget.Edit', {
    extend: 'Ext.window.Window',
    alias : 'widget.budgetedit',

    title : 'Budget',
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
            id   : 'budget-name',
            name : 'name',
            allowBlank: false,
            hideLabel: true,
            emptyText: 'Budget name'
          }, {
            xtype           : 'numberfield',
            vtype           : 'year',
            id              : 'budget-year',
            hideLabel       : true,
            emptyText       : 'Year',
            decimalPrecision: 0,
            name            : 'year',
            value           : (new Date()).getFullYear()
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
