Ext.regController('Receipt', {
  index: function() {
    if (!this.receiptView) {
      this.receiptView = this.render({
        xtype: 'receipts',
      });
    }
 
    this.application.viewport.setActiveItem(this.receiptView);
  },
});
