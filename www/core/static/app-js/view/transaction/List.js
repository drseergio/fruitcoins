Ext.define('moneypit.view.transaction.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.transactionlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No transactions yet.. Did you know that you can import transactions from <b>CSV</b> files using <b>Upload</b>?</div>',
    deferEmptyText: false,
  },
  initComponent: function() {
    this.selModel = Ext.create('Ext.selection.CheckboxModel');
    this.columns = [{
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          xtype     : 'datefield',
          flex      : 1,
          format    : 'Y-m-d',
          allowBlank: false
        }
      }, {
        header      : 'Description',
        dataIndex   : 'description',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          flex: 2
        }
      }, {
        header      : 'Type',
        dataIndex   : 'type',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Category',
        dataIndex   : 'category_id',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          xtype       : 'combo',
          displayField: 'name',
          selectOnFocus: true,
          valueField  : 'id',
          emptyText   : 'Category',
          store       : 'CategorySearch',
          name        : 'category_id',
          minChars    : 0,
          flex        : 1
        },
        renderer      : function(value, metaData, record) {
          return record.get('category');
        }
      }, {
        header      : 'Amount',
        dataIndex   : 'amount',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          xtype     : 'numberfield',
          minValue  : 0.01,
          flex      : 1
        },
      }
    ];
    this.plugins = [
        Ext.create('Ext.ux.RowDropZone'),
        Ext.create('Ext.grid.plugin.RowEditing', {
          clicksToMoveEditor: 1,
          autoCancel        : false,
          pluginId          : 'rowEditing'
        })];
    this.store = 'Transaction';
    this.features = [Ext.create('Ext.grid.feature.Grouping', {
      groupHeaderTpl: '{name} ({rows.length} {[values.rows.length > 1 ? "items" : "item"]})'
    })];
    this.tbar = [{
        id      : 'tbar-new',
        text    : 'New..',
        action  : 'new',
        iconCls : 'icons-add',
        disabled: true
      }, {
        id      : 'tbar-delete',
        text    : 'Delete',
        action  : 'delete',
        iconCls : 'icons-delete',
        disabled: true
      }, {
        id      : 'tbar-tags',
        text    : 'Tags',
        disabled: true,
        iconCls : 'icons-tag',
        menu    : {
          xtype: 'menu',
          id   : 'tagsmenu',
          plain: true,
          items: [{ text: 'unassign' }]
        }
      }, {
        id      : 'tbar-categories',
        text    : 'Assign to',
        disabled: true,
        iconCls : 'icons-category',
        menu    : {
          xtype: 'menu',
          id   : 'categoriesmenu',
          plain: true,
          items: [{ text: 'unassign' }]
        }
      }, {
        id      : 'tbar-download',
        text    : 'Save as',
        action  : 'save-as',
        iconCls : 'icons-download',
        disabled: true,
        menu    : {
          xtype: 'menu',
          id   : 'downloadmenu',
          plain: true,
          items: [{
              id: 'csv-export',
              text: '.csv (Spreadsheet)',
              iconCls : 'icons-csv',
              style: 'text-align: "left"',
          }]
        }
      }, {
        id      : 'tbar-upload',
        text    : 'Upload',
        action  : 'upload',
        iconCls : 'icons-upload',
        disabled: true
    }];
    this.bbar = Ext.create('Ext.PagingToolbar', ({
      store      : 'Transaction',
      displayInfo: true,
      displayMsg : 'Displaying transactions {0} - {1} of {2}',
      emptyMsg   : "No transactions to display",
    }));
    this.callParent(arguments);
  }
});
