Ext.define('moneypit.view.account.Edit', {
    extend: 'Ext.window.Window',
    alias : 'widget.accountedit',

    title : 'Account',
    layout: 'fit',
    autoShow: true,
    border  : false,
    modal   : true,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        border: false,
        frame: true,
        items: [{
            xtype: 'textfield',
            id   : 'account-name',
            name : 'name',
            allowBlank: false,
            hideLabel: true,
            emptyText: 'Account name'
          }, {
            xtype       : 'combo',
            id          : 'account-type',
            store       : 'AccountType',
            hideLabel   : true,
            name        : 'type',
            hidden      : true,
            queryMode   : 'local',
            displayField: 'text',
            valueField  : 'value',
            editable    : false,
            value       : 1,
          }, {
            id           : 'account-currency',
            xtype        : 'fxcombobox',
            hideLabel    : true,
            name         : 'currency',
            valueField   : 'id',
            displayField : 'symbol',
            triggerAction: 'all',
            hidden       : true,
            queryMode   : 'local',
            hiddenName   : 'currency',
            editable     : false,
            allowBlank   : false
          }, {
            xtype           : 'numberfield',
            id              : 'account-balance',
            hideLabel       : true,
            emptyText       : 'Opening balance',
            decimalPrecision: 2,
            name            : 'opening_balance',
            hideTrigger     : true,
            hidden          : true
          }, {
            xtype           : 'datefield',
            id              : 'account-date',
            emptyText       : 'Date',
            format          : 'Y-m-d',
            allowBlank      : false,
            hideLabel       : true,
            name            : 'opened_date',
            value           : new Date(),
            hidden          : true
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
