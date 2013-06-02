Ext.regController('Transaction', {
  index: function(options) {
    if (!options.account) {
      Ext.redirect('Account/index');
    }

    if (!this.transactionView) {
      this.transactionView = this.render({
        xtype: 'transactions',
        account: this.selectedAccount,
        listeners: {
          deactivate: function(view){
            view.destroy();
            delete this.transactionView;
          },
          scope: this
        }
      });
    }

    var store = this.transactionView.store;
    var account = options.account;
    store.proxy.extraParams = {
      id: account.get('id'),
      start: 0
    };
    store.load();

    this.application.viewport.setActiveItem(this.transactionView, options.animation);
  }
});
