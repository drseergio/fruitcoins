Ext.define('moneypit.view.liberation.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.liberation',
  border       : false,
  viewConfig: {
    emptyText: '<div class="emptyText">Once you upload a file this list will be populated with items preview. You will have a chance to preview the data before finally accepting it</div>',
    deferEmptyText: false,
  },

  initComponent: function() {
    this.columns = [{
        header      : 'Description',
        dataIndex   : 'description',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
    }];
    this.tbar = [{
        id      : 'liberation-import',
        text    : 'Import',
        action  : 'import',
        iconCls : 'icons-import',
      }, {
        id      : 'liberation-export',
        text    : 'Export',
        iconCls : 'icons-export',
        menu    : {
          xtype: 'menu',
          plain: true,
          items: [{
            text   : 'KMyMoney',
            iconCls: 'icons-kmymoney',
            handler: function() {
              window.open('api/liberation/export/kmy', '_blank');
            }
          }]
        }
   }];
   this.bbar = [{
        id      : 'liberation-commit',
        text    : 'Commit',
        action  : 'commit',
        iconCls : 'icons-commit',
        disabled: true
      }, {
        id      : 'liberation-discard',
        text    : 'Discard',
        action  : 'discard',
        iconCls : 'icons-delete',
        disabled: true
    }];
    this.store = 'Import';
    this.features = [Ext.create('Ext.grid.feature.Grouping', {
      startCollapsed: true,
      groupHeaderTpl: '{name} ({rows.length} {[values.rows.length > 1 ? "items" : "item"]})'
    })];
    this.callParent(arguments);
  }
});
