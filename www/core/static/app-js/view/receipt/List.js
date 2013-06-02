Ext.define('moneypit.view.receipt.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.receiptlist',
  border       : false,
  cls          : 'sidebar-toolbar',
  initComponent: function() {
    this.store = 'Receipt';
    this.stripeRows = true;
    this.hideHeaders = true;
    this.tbar = [{
        text    : 'Delete all',
        iconCls : 'icons-delete',
        action  : 'delete-all'
    }];
    this.columns = [{
        flex     : 8,
        id       : 'receiptColumn',
        dataIndex: 'date',
      }, {
        flex     : 3,
        xtype    : 'actioncolumn',
        items    : [{
          id  : 'icons-delete',
          icon: staticPath + '/resources/images/icons/delete.png',
        }]
    }];
    this.callParent(arguments);
  },

  viewConfig: {
    emptyText: '<div class="emptyText">Upload receipts using your mobile and view them here</div>',
    deferEmptyText: false,
  }
});
