Ext.define('moneypit.view.transaction.Add', {
  extend       : 'Ext.window.Window',
  alias        : 'widget.transactionadd',
 
  title        : 'Enter new transaction',
  layout       : 'fit',
  autoShow     : true,
  modal        : true,
  width        : 400,
  closable     : true,

  initComponent: function() {
    this.items = [{
      xtype : 'form',
      frame : true,
      border: false,
      layout: 'anchor',

      items : [{
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype       : 'combo',
              id          : 'combo-category-type',
              hideLabel   : true,
              columnWidth : .5,
              name        : 'type',
              queryMode   : 'local',
              displayField: 'text',
              valueField  : 'value',
              anchor      : '100%',
              editable    : false,
              value       : 1,
              store       : 'TransactionType'
            }, {
              xtype       : 'combo',
              id          : 'combo-category',
              hideLabel   : true,
              columnWidth : .5,
              displayField: 'name',
              selectOnFocus: true,
              valueField  : 'id',
              emptyText   : 'Category',
              store       : 'CategorySearch',
              name        : 'category_id',
              anchor      : '100%',
              minChars    : 0,
            }, {
              xtype       : 'combo',
              id          : 'combo-account',
              hideLabel   : true,
              columnWidth : .5,
              displayField: 'name',
              valueField  : 'id',
              emptyText   : 'Account',
              store       : 'Account',
              name        : 'account_id',
              anchor      : '100%',
              hidden      : true,
              minChars    : 0
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              id              : 'transaction-amount',
              columnWidth     : .4,
              hideLabel       : true,
              emptyText       : 'Amount',
              decimalPrecision: 2,
              name            : 'amount',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 0.01
            }, {
              xtype           : 'numberfield',
              emptyText       : 'Conversion rate',
              disabled        : true,
              name            : 'rate',
              id              : 'transaction-rate',
              hideTrigger     : true,
              decimalPrecision: 4,
              columnWidth     : .3,
              minValue        : 0
            }, {
              xtype           : 'numberfield',
              disabled        : true,
              emptyText       : 'OR final amount',
              name            : 'final',
              hideTrigger     : true,
              id              : 'transaction-final',
              decimalPrecision: 2,
              columnWidth     : .3,
              minValue        : 0.01
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'datefield',
              id              : 'transaction-date',
              columnWidth     : .3,
              emptyText       : 'Date',
              format          : 'Y-m-d',
              allowBlank      : false,
              hideLabel       : true,
              name            : 'date',
              value           : new Date()
            }, {
              xtype           : 'textfield',
              id              : 'transaction-description',
              hideLabel       : true,
              columnWidth     : .7,
              emptyText       : 'Description...',
              name            : 'description',
              anchor          : '100%'
          }]
        }, {
          xtype      : 'fieldset',
          title      : 'Tags',
          layout     : 'anchor',
          defaults   : {
            anchor    : '100%',
            labelStyle: 'padding-left:4px;'
          },
          collapsible: true,
          collapsed  : true,
          items      : [{
            xtype  : 'checkboxgroup',
            id     : 'transaction-tags',
            cls    : 'x-check-group-alt',
            columns: 2,
            items  : []
          }]
      }]
    }];

    this.buttons = [{
        text   : 'Save',
        action : 'save'
      }, {
        text   : 'Cancel',
        scope  : this,
        handler: this.close
    }];
 
    this.callParent(arguments);
  }
});
