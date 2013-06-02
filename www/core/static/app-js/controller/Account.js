Ext.define('moneypit.controller.Account', {
  extend          : 'Ext.app.Controller',
  views           : [ 'account.Edit', 'account.List', 'fx.Combobox' ],
  stores          : [ 'Account', 'AccountType', 'Currency' ],
  models          : [ 'Account', 'Currency' ],

  refs: [{
      selector: 'accountlist',
      ref     : 'accountList'
    }, {
      selector: 'accountedit',
      ref     : 'accountEdit'
  }],

  init            : function() {
    this.control({
      'accountlist': {
        cellclick: this.openTransactions
      },
      'accountlist actioncolumn': {
        click: this.onActionColumn
      },
      'accountlist button[action=showwealth]': {
        click : this.openWealth
      },
      'accountedit button[action=save]': {
        click: this.saveAccount
      },
      'accountlist button[action=new]': {
        click: this.newAccount
      },
      'accountedit #account-name': {
        afterrender: this.setFocus,
        specialkey: this.onAddKey
      },
      'accountedit #account-type': {
        render: this.populateTypes
      },
      'accountedit #account-currency': {
        render: this.setCurrency
      }
    });
    this.application.on({
      loadtransactions : this.onLoadTransactions,
      addtransaction   : this.onAddTransaction,
      deletetransaction: this.onDeleteTransaction,
      scope            : this
    });
  },

  onAddTransaction   : function(account) {
  },

  onDeleteTransaction: function(account) {
  },

  onLoadTransactions : function() {
    var list = this.getAccountList();
    list.getSelectionModel().deselectAll();
  },

  onActionColumn  : function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var action = e.target.getAttribute('class');
    if (action.indexOf("x-action-col-0") != -1) {
      this.editAccount(rec);
    } else if (action.indexOf("x-action-col-1") != -1) {
      this.deleteAccount(rec);
    }
  },

  onAddKey           : function(field, e) {
    if (e.getKey() == e.ENTER) {
      this.saveAccount();
    }
  },

  populateTypes: function(combo) {
    combo.setValue(2);
  },

  setCurrency: function(combo) {
    combo.setValue(wealthCurrencyId);
  },

  newAccount: function() {
    var view = Ext.widget('accountedit');
    var form = view.down('form');
    form.down('#account-type').show();
    form.down('#account-currency').show();
    form.down('#account-balance').show();
    form.down('#account-date').show();
  },

  editAccount: function(record) {
    var view = Ext.widget('accountedit');
    var form = view.down('form');
    form.loadRecord(record);
  },

  deleteAccount: function(record) {
    var store = this.getAccountStore();
    var app = this.application;
    Ext.MessageBox.confirm('Confirm', 'Are you sure you want to do that?', function(btn) {
      if (btn == 'yes') {
        var id = record.get('id');
        record.unjoin(store)
        record.destroy({
          success: function() {
            app.fireEvent('deleteaccount', id);
            store.load();
          }
        });
      }
    });
  },

  saveAccount: function() {
    var win = this.getAccountEdit();
    var store = this.getAccountStore();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();

    if (record) {
      record.unjoin(store);
    } else {
      record = Ext.create('moneypit.model.Account');
    }
    record.set(values);
    var app = this.application;

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          store.load({
            callback: function() {
              win.close();
              app.fireEvent('editaccount', rec.get('id'));
            }
          });
        },
        failure: function(rec, op) {
          form.el.unmask();
          var errors = op.request.scope.reader.jsonData['errors'];
          form.getForm().markInvalid(errors);
        },
      });
    }
  },

  openTransactions: function(iView, iCellEl, iColIdx, record, iRowEl, iRowIdx, iEvent) {
    var fieldName = iView.getGridColumns()[iColIdx].dataIndex;

    if (fieldName == 'name') {
      var transactionController = this.getController('Transaction');
      transactionController.openAccount(record.get('id'));
    }
  },

  openWealth: function() {
    var transactionController = this.getController('Transaction');
    transactionController.openWealth();
  },

  setFocus: function(field) {
    field.focus(false, 800);
  },
});
