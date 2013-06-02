Ext.regController('Account', {
  index: function() {
    if (!this.indexView) {
      this.indexView = this.render({
        xtype: 'accounts',
        listeners: {
          itemtap: function(view, index) {
            Ext.dispatch({
              account: view.store.getAt(index),
              controller: 'Transaction',
              action: 'index',
              historyUrl: 'Account/index',
              animation: {
                type: 'slide',
                reverse: false,
              },
            });
          },
          scope: this
        }
      });
    }
    var store = Ext.getStore('Account');
    store.load();
 
    this.application.viewport.setActiveItem(this.indexView);
  },
});
