Ext.define('moneypit.controller.Receipt', {
  extend: 'Ext.app.Controller',
  views : [ 'receipt.List' ],
  stores: [ 'Receipt' ],
  models: [ 'Receipt' ],

  refs: [{
      selector: 'receiptlist',
      ref     : 'receiptList'
  }],

  init            : function() {
    this.control({
      'receiptlist': {
        cellclick: this.openReceipt
      },
      'receiptlist button[action=delete-all]': {
        click: this.deleteAll
      },
      'receiptlist actioncolumn': {
        click    : this.onActionColumn
      },
    });
  },

  onActionColumn  : function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var action = e.target.getAttribute('class');
    if (action.indexOf("x-action-col-0") != -1) {
      this.deleteReceipt(rec);
    }
  },

  openReceipt: function(iView, iCellEl, iColIdx, record, iRowEl, iRowIdx, iEvent) {
    var fieldName = iView.getGridColumns()[iColIdx].dataIndex;

    if (fieldName == 'date') {
      var win = Ext.create('Ext.window.Window', {
        height: 250,
        width: 250,
        layout: 'fit',
        items: [{
          xtype: 'image',
          src: '/api/receipt/image?id=' + record.get('id')
        }]
      });
      win.show();
    }
  },

  deleteAll: function() {
    var store = this.getReceiptStore();
    Ext.MessageBox.confirm('Confirm', 'Are you sure you want to do that?', function(btn) {
      if (btn == 'yes') {
        store.each(function(record){store.remove(record);});
        store.sync();
      }
    });
  },

  deleteReceipt: function(record) {
    var store = this.getReceiptStore();
    store.remove(record);
    store.sync();
  }
});
