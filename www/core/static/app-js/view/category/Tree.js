Ext.define('moneypit.view.category.Tree', {
  extend       : 'Ext.tree.Panel',
  alias        : 'widget.categorytree',
  border       : false,

  viewConfig: {
    plugins: {
      ptype: 'treeviewdragdrop'
    }
  },

  initComponent: function() {
    this.store = 'Category';
    this.rootVisible = false;
    this.tbar = [{
        id      : 'category-new',
        text    : 'New..',
        iconCls : 'icons-add',
        action  : 'new',
        disabled: true
      }, {
        id      : 'category-delete',
        text    : 'Delete',
        action  : 'delete',
        iconCls : 'icons-delete',
        disabled: true
      }, {
        id      : 'category-rename',
        text    : 'Rename',
        action  : 'edit',
        iconCls : 'icons-edit',
        disabled: true
      }, {
        id      : 'category-refresh',
        action  : 'refresh',
        iconCls : 'icons-refresh',
    }];
    this.amountRender = function(value, metaData, record) {
      if (value == '-') return value;

      var amount = parseFloat(value);
      if (amount < 0) {
        return '<span style="color:green;">' + Math.abs(amount).toFixed(2) + '</span>';
      } else if (amount > 0) {
        return '<span style="color:red;">' + Math.abs(value).toFixed(2) + '</span>';
      } else {
        return '0.00';
      }
    };
    this.columns = [{
        xtype: 'treecolumn',
        id: 'categoryColumn',
        text: 'Name',
        flex: 4,
        dataIndex: 'text'
      },{
        text: 'Description',
        id: 'categoryDescription',
        flex: 2,
        dataIndex: 'description'
      }, {
        text: 'Balance',
        id  : 'categoryBalance',
        flex: 1,
        dataIndex: 'balance',
        renderer: this.amountRender
      }, {
        text: 'Total',
        id  : 'categoryTotal',
        flex: 1,
        dataIndex: 'total_balance',
        renderer: this.amountRender
    }];
    this.callParent(arguments);
  }
});
