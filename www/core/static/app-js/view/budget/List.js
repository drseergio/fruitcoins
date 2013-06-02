Ext.define('moneypit.view.budget.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.budgetlist',
  layout       : 'fit',
  border       : false,
  viewConfig: {
    emptyText: '<div class="emptyText">No budget lines created yet</div>',
    deferEmptyText: false,
  },

  initComponent: function() {
    this.selModel = Ext.create('Ext.selection.CheckboxModel');
    this.columns = [{
        header      : 'Category',
        dataIndex   : 'category_id',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          xtype       : 'combo',
          displayField: 'name',
          valueField  : 'id',
          emptyText   : 'Category',
          store       : 'CategorySearch',
          name        : 'category_id',
          flex        : 1,
          minChars    : 0,
        },
        renderer      : function(value, metaData, record) {
          return record.get('category');
        }
      }, {
        header      : 'Period',
        dataIndex   : 'period',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          xtype       : 'combo',
          id          : 'period-combo',
          hideLabel   : true,
          emptyText   : 'Period',
          name        : 'type',
          flex        : 1,
          queryMode   : 'local',
          displayField: 'text',
          valueField  : 'value',
          editable    : false,
          store       : 'Period'
       },
      }, {
        header      : 'Budgeted',
        dataIndex   : 'amount',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          flex      : 1,
          xtype     : 'numberfield',
          minValue  : 0.01,
        },
      }, {
        header      : 'Total budgeted',
        dataIndex   : 'total_amount',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
       }, {
        header      : 'So far',
        dataIndex   : 'balance',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        renderer    : function(value, metaData, record) {
          if (record.get('type') == 1) {
            var fvalue = parseFloat(value) * -1;
            return fvalue.toFixed(2);
          }
          return value.toFixed(2);
        }
      }
    ];
    this.plugins = [
        Ext.create('Ext.grid.plugin.RowEditing', {
          clicksToMoveEditor: 1,
          autoCancel        : false,
          pluginId          : 'rowEditing'
        })];
    this.store = 'BudgetLine';
    this.tbar = [{
        id      : 'tbar-budget-new',
        text    : 'Create',
        action  : 'new',
        iconCls : 'icons-budget_add',
      }, {
        xtype: 'combo',
        id: 'budget-combo',
        hideLabel: true,
        store: 'Budget',
        displayField: 'name',
        valueField: 'id',
        queryMode: 'local',
        editable: false,
        triggerAction: 'all',
        emptyText: 'Select budget',
        width: 135,
        disabled: true
      }, {
        id      : 'tbar-budget-delete',
        text    : 'Delete',
        action  : 'delete',
        iconCls : 'icons-budget_delete',
        disabled: true
      }, '-', {
        id      : 'tbar-budget-new-line',
        text    : 'New..',
        action  : 'new-line',
        iconCls : 'icons-add',
        disabled: true
      }, {
        id      : 'tbar-budget-delete-line',
        text    : 'Delete',
        action  : 'delete-line',
        iconCls : 'icons-delete',
        disabled: true
      }, {
        action  : 'refresh',
        iconCls : 'icons-refresh',
        disabled: true
    }];
    this.callParent(arguments);
  }
});
