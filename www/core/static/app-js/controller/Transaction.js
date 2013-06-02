Ext.define('moneypit.controller.Transaction', {
  extend        : 'Ext.app.Controller',
  views         : [
    'transaction.Add',
    'transaction.List',
    'transaction.Summary',
    'transaction.Upload' ],
  stores        : [
    'Account',
    'AccountSearch',
    'Category',
    'CategorySearch',
    'Tag',
    'Transaction',
    'TransactionType' ],
  models        : [
    'AccountSearch',
    'CategorySearch',
    'Transaction',
    'Wealth' ],

  refs: [{
      selector: 'summarypanel',
      ref     : 'summaryPanel'
    }, {
      selector: 'transactionlist',
      ref     : 'transactionList'
    }, {
      selector: 'transactionadd',
      ref     : 'transactionAdd'
    }, {
      selector: 'upload',
      ref     : 'uploadWindow'
  }],

  init          : function () {
    this.control({
      'transactionlist'                        : {
        render         : this.onRender,
        selectionchange: this.onSelectionChange,
        tagassociated  : this.onTagAssociated,
        beforeedit     : this.onBeforeEdit,
        edit           : this.onEdit,
      },
      'transactionlist *'                      : {
        itemkeydown    : this.onItemKeyDown
      },
      'accountlist': {
        newtransfer    : this.onNewTransfer,
      },
      'transactionlist #tagsmenu'              : {
        beforeshow     : this.populateTags
      },
      'transactionlist #categoriesmenu'        : {
        beforeshow     : this.populateCategories
      },
      'transactionlist button[action=new]' : {
        click: this.openAddTransaction
      },
      'transactionlist button[action=delete]'  : {
        click: this.deleteTransaction
      },
      'transactionlist button[action=upload]'  : {
        click: this.upload
      },
      'upload button[action=upload]' : {
        click: this.uploadTransactions
      },
      '#downloadmenu #csv-export'  : {
        click: this.exportCsv
      },
      'transactionadd #combo-category'         : {
        afterrender: function(field) {
          Ext.defer(this.setFocus, 100, this, [field]);
        }
      },
      'transactionadd #transaction-amount'     : {
        specialkey: this.onAddKey
      },
      'transactionadd #transaction-date'       : {
        specialkey: this.onAddKey
      },
      'transactionadd #transaction-description': {
        specialkey: this.onAddKey
      },
      'transactionadd #combo-category-type'    : {
        select: this.changeType
      },
      'transactionadd #combo-account'          : {
        select: this.setCurrency
      },
      'transactionadd button[action=save]'     : {
        click: this.saveTransaction
      },
      'transactionadd'                         : {
        destroy: this.focusTransactions
      },
    });
    this.application.on({
      addtransaction   : this.onAddTransaction,
      edittag          : this.onEditTag,
      editaccount      : this.onEditAccount,
      deletetag        : this.onDeleteTag,
      deleteaccount    : this.onDeleteAccount,
      loadtransactions : this.onLoadTransactions,
      deletetransaction: this.onDeleteTransaction,
      scope            : this
    });
    this.getTransactionStore().on({
      load             : this.onLoadStore,
      scope            : this
    });
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getTransactionTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val - 1);
      return type.data.text;
    };
    column = list.down('[dataIndex=amount]');
    column.renderer = this.amountRenderer;
    this.openWealth();
  },

  onLoadStore: function(store) {
    this.focusTransactions();
    var list = this.getTransactionList();
    if (store.getCount() > 0) {
      list.down('button[action=save-as]').enable();
    } else {
      list.down('button[action=save-as]').disable();
    }
  },

  onLoadTransactions : function(type, id) {
    var list = this.getTransactionList();
    var buttonNew = list.down('#tbar-new');
    var buttonUpload = list.down('button[action=upload]');
    var data = {};

    this.type = type;
    this.id = id;

    if (type == 'account') {
      buttonNew.enable();
      buttonUpload.enable();
      this.selected_account = id;
    } else {
      this.selected_account = null;
      buttonNew.disable();
      buttonUpload.disable();
    }

    this.updateSummary(type, id);
  },

  onAddTransaction   : function() {
    this.updateSummary(this.type, this.id);
  },

  onDeleteTransaction: function() {
    this.updateSummary(this.type, this.id);
  },

  onEditTag: function(id) {
    if (this.type == 'tag' && this.id == id) {
      this.updateSummary(this.type, this.id);
    }
  },

  onEditAccount: function(id) {
    if (this.type == 'account' && this.id == id) {
      this.updateSummary(this.type, this.id);
    }
  },

  onDeleteTag: function(id) {
    if (this.type == 'tag' && this.id == id) {
      this.openWealth();
    }
    Ext.example.msg(
        'Deleted',
        'Successfully deleted tag');
  },

  onDeleteAccount: function(id) {
    if (this.type == 'account' && this.id == id) {
      this.openWealth();
    } else if (this.type == 'wealth') {
      this.updateSummary(this.type, this.id);
      this.getTransactionStore().load();
    }
    Ext.example.msg(
        'Deleted',
        'Successfully deleted account');
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getTransactionList();
    var del = win.down('button[action=delete]');
    var tag = win.down('#tbar-tags');
    var category = win.down('#tbar-categories');

    if (model.hasSelection()) {
      del.enable();
      var hasTransfer = false;
      model.getSelection().forEach(function(record) {
        if (record.get('type') == 3) {
          hasTransfer = true;
        }
      });
      if (!hasTransfer) {
        tag.enable();
        category.enable();
      } else {
        tag.disable();
        category.disable();
      }
    } else {
      del.disable();
      category.disable();
      tag.disable();
    }
  },

  onAddKey           : function(field, e) {
    if (e.getKey() == e.ENTER) {
      this.saveTransaction()
    }
  },

  onTagAssociated    : function(associate, tag_id, transactions) {
    var transaction_ids = [];
    var tagStore = this.getTagStore();

    transactions.forEach(function(id) {
      transaction_ids.push(id);
    });
    var me = this;
    Ext.Ajax.request({
      method  : 'POST',
      jsonData: {
        associate   : associate,
        tag         : tag_id,
        transactions: transaction_ids
      },
      url     : '/api/transaction/associate',
      success : function (resp) {
        me.getTransactionStore().load({
          callback: function() {
            me.updateSummary(me.type, me.id);
          }
        });
        if (associate) {
          var tag = tagStore.getById(tag_id);
        
          Ext.example.msg(
              'Associated',
              'Successfully associated tag "{0}"', tag.get('name'));
        } else {
          Ext.example.msg(
              'Removed tag',
              'Successfully removed tag from transactions');
        }
      }
    });
  },

  onBeforeEdit     : function(e) {
    var form = e.grid.getPlugin('rowEditing').editor.form;
    var field = form.findField('category_id');
    if (e.record.get('type') == 3) {
      field.disable();
    } else {
      this.getCategorySearchStore().load();
      field.enable();

      var category_id = e.record.get('category_id');
      field.setValue(category_id);
    }
  },

  onEdit           : function(e) {
    if (e.record.get('type') == 1 || e.record.get('type') == 2) {
      var field = e.grid.getPlugin('rowEditing').editor.form.findField('category_id');
      var value = field.getValue();
      var record = field.getStore().getById(value)
      if (record) {
        e.record.set('category', record.get('name'));
      }
    } else {
      e.record.set('account_from', this.selected_account);
    }
    e.store.mySync({
      scope   : this,
      callback: function() {
        this.updateSummary(this.type, this.id);
      }
    });
  },

  onNewTransfer    : function(id_from, id_to) {
    if (this.type != 'account' || this.selected_account != id_from) {
      this.openAccount(id_from);
    }
    var view = Ext.widget('transactionadd');
    var form = view.down('form');
    var typeCombo = form.down('#combo-category-type').setValue(3);
    form.down('#combo-account').setValue(id_to);
    this.changeType(typeCombo);
  },

  onItemKeyDown    : function(grid, rec, item, idx, e, opts) {
    if (e.shiftKey && e.keyCode == 88) {
      console.log('DELETE TRANSACTION');
    }
    if (!e.ctrlKey && !e.altKey && !e.shiftKey) {
      var store = this.getTransactionStore();
      if (e.keyCode == 68) {
        var view = Ext.widget('transactionadd');
        var form = view.down('form');
        var record = Ext.create('moneypit.model.Transaction', {
          type: 2,
          date: new Date()
        });
        form.loadRecord(record);
        var typeCombo = form.down('#combo-category-type').setValue(2);
        this.getTagStore().each(function (record) {
          var checkboxes = form.down('#transaction-tags');
          checkboxes.add({
            boxLabel: record.get('name'),
            name    : 'tag-' + record.get('id')
          });
        });
      } else if (e.keyCode == 87) {
        var view = Ext.widget('transactionadd');
        var form = view.down('form');
        var record = Ext.create('moneypit.model.Transaction', {
          type: 1,
          date: new Date()
        });
        form.loadRecord(record);
        var typeCombo = form.down('#combo-category-type').setValue(1);
        this.getTagStore().each(function (record) {
          var checkboxes = form.down('#transaction-tags');
          checkboxes.add({
            boxLabel: record.get('name'),
            name    : 'tag-' + record.get('id')
          });
        });
     } else if (e.keyCode == 84) {
        var view = Ext.widget('transactionadd');
        var form = view.down('form');
        var record = Ext.create('moneypit.model.Transaction', {
          type: 3,
          date: new Date()
        });
        form.loadRecord(record);
        var typeCombo = form.down('#combo-category-type').setValue(3);
        this.getTagStore().each(function (record) {
          var checkboxes = form.down('#transaction-tags');
          checkboxes.add({
            boxLabel: record.get('name'),
            name    : 'tag-' + record.get('id')
          });
        });
        this.changeType(typeCombo);
      } else if (e.keyCode == 82) {
        store.load();
      } else if (e.keyCode == 78) {
        store.nextPage();
      } else if (e.keyCode == 80 && store.currentPage > 1) {
        store.previousPage();
      }
    }
  },

  focusTransactions: function() {
    var list = this.getTransactionList();
    var store = this.getTransactionStore();
    var selection = list.getSelectionModel();
    list.getView().focus();
    if (!selection.hasSelection() && store.getCount() > 0) {
      selection.select(0);
    }
  }, 

  updateSummary    : function(type, id) {
    var panel = this.getSummaryPanel();
    var me = this;
    if (type == 'account') {
      var Model = Ext.ModelManager.getModel('moneypit.model.Account');
    } else if (type == 'category') {
      var Model = Ext.ModelManager.getModel('moneypit.model.Category');
    } else if (type == 'tag') {
      var Model = Ext.ModelManager.getModel('moneypit.model.Tag');
    } else {
      var Model = Ext.ModelManager.getModel('moneypit.model.Wealth');
      id = 0;
    }
    Model.load(id, {
      success: function(obj) {
        if (me.type == type) {
          obj.update_summary(panel);
        }
      }
    });
  },

  openAccount   : function(id) {
    var tabpanel = Ext.ComponentQuery.query("#app-center")[0];
    tabpanel.setActiveTab("app-center-transactions");

    var store = this.getTransactionStore();
    store.getProxy().url = '/api/transaction/account';
    store.getProxy().extraParams = { id: id };
    var me = this;
    store.load({
      callback: function() {
        me.application.fireEvent('loadtransactions', 'account', id);
      }
    });
  },

  openWealth    : function() {
    var tabpanel = Ext.ComponentQuery.query("#app-center")[0];
    tabpanel.setActiveTab("app-center-transactions");

    var store = this.getTransactionStore();
    store.getProxy().url = '/api/transaction/wealth';
    store.getProxy().extraParams = {};
    var me = this;
    store.load({
      callback: function() {
        me.application.fireEvent('loadtransactions', 'wealth');
      }
    });
  },

  openCategory  : function(id) {
    var tabpanel = Ext.ComponentQuery.query("#app-center")[0];
    tabpanel.setActiveTab("app-center-transactions");

    var store = this.getTransactionStore();
    store.getProxy().url = '/api/transaction/category';
    store.getProxy().extraParams = { id: id };
    var me = this;
    store.load({
      callback: function() {
        me.application.fireEvent('loadtransactions', 'category', id);
      }
    });
  },

  openTag       : function(id) {
    var tabpanel = Ext.ComponentQuery.query("#app-center")[0];
    tabpanel.setActiveTab("app-center-transactions");

    var store = this.getTransactionStore();
    store.getProxy().url = '/api/transaction/tag';
    store.getProxy().extraParams = { id: id };
    var me = this;
    store.load({
      callback: function() {
        me.application.fireEvent('loadtransactions', 'tag', id);
      }
    });
  },

  setFocus: function(field) {
    var form = field.up('form');
    var combo = form.down('#combo-category-type');
    var comboAccount = form.down('#combo-account');
    if (combo.getValue() == 3) {
      if (comboAccount.getValue()) {
        var amount = form.down('#transaction-amount');
        amount.focus(false, 400);
      } else {
        comboAccount.focus(false, 400);
      }
    } else {
      field.focus(false, 400);
    }
  },

  openAddTransaction: function() {
    var view = Ext.widget('transactionadd');
    var record = Ext.create('moneypit.model.Transaction', {
      type: 1,
      date: new Date()
    });
    var form = view.down('form');
    form.loadRecord(record);
    this.getTagStore().each(function (record) {
      var checkboxes = form.down('#transaction-tags');
      checkboxes.add({
        boxLabel: record.get('name'),
        name    : 'tag-' + record.get('id')
      });
    });
  },

  deleteTransaction: function() {
    var list = this.getTransactionList();
    var store = this.getTransactionStore();
    var model = list.getSelectionModel();
    model.selected.each(function(item) {
      store.remove(item);
    });
    store.mySync({
      scope   : this,
      callback: function() {
        this.application.fireEvent('deletetransaction', 'account', this.selected_account);
      }
    });
  },

  populateTags: function(menu) {
    menu.removeAll();
    var tagStore = this.getTagStore();
    var controller = this;

    var list = this.getTransactionList();
    var model = list.getSelectionModel();
    var selected = model.getSelection();

    tagStore.each(function(record) {
      var checked = true;
      var has_checked = false;
      var cls = '';

      selected.forEach(function(transaction) {
        var tags = transaction.tags().data.items;
        var has_tag = false;
        tags.forEach(function(tag) {
          if (tag.get('id') == record.get('id')) {
            has_tag = true;
            has_checked = true;
          }
        });
        if (!has_tag) {
          checked = false;
        }
      });
      if (!checked && has_checked) {
        checked = true;
        cls = 'tag-some-associated';
      }
      menu.add({
        text   : record.get('name'),
        checked: checked,
        cls    : cls,
        handler: function(e) {
          controller.associateTag(e, record, selected);
          menu.hide();
        }
      });
    });

    menu.add('-');
    menu.add({
      text   : 'Deassociate all..',
      handler: function(e) {
        controller.deAssociate();
        menu.hide();
      }
    });
  },

  populateCategories: function(menu) {
    menu.removeAll();
    var categoryStore = this.getCategoryStore();
    var controller = this;

    var root = categoryStore.getRootNode();
    this.populateCategory(root, menu, menu);
  },

  populateCategory: function(node, menu, top_menu) {
    var me = this;
    node.childNodes.forEach(function(child) {
      if (child.get('id') == 'inc' || child.get('id') == 'exp') {
        var handler = function() {return false;};
        var hideOnClick = false;
      } else {
        var handler = function() {
          me.assignCategory(child);
        };
        var hideOnClick = true;
      }
 
      if (!child.childNodes.length) {
        menu.add({
          text   : child.get('text'),
          iconCls: child.get('iconCls'),
          handler: handler
        });
      } else {
        var childMenu = Ext.create('Ext.menu.Menu', {});
        me.populateCategory(child, childMenu, top_menu);
        menu.add({
          hideOnClick: hideOnClick,
          text       : child.get('text'),
          iconCls    : child.get('iconCls'),
          menu       : childMenu,
          handler    : handler
        });
      }
    });
  },

  assignCategory: function(category) {
    var list = this.getTransactionList();
    var model = list.getSelectionModel();
    var selected = model.getSelection();
    var store = this.getTransactionStore();

    selected.forEach(function(transaction) {
      transaction.set('category_id', category.get('id'));
    });

    store.mySync({
      scope   : this,
      callback: function() {
        this.updateSummary(this.type, this.id);
        store.load();
      }
    });
  },

  amountRenderer: function(value, metaData, record) {
    if (record.get('type') == 2) {
      return '<span style="color:green;">' + value.toFixed(2) + '</span>';
    } else if (record.get('type') == 1) {
      return '<span style="color:red;">' + value.toFixed(2) + '</span>';
    } else {
      if (record.get('amount_real') < 0) {
        return '<span style="color:red;">' + value.toFixed(2) + '</span>';
      } else {
        return '<span style="color:green;">' + value.toFixed(2) + '</span>';
      }
    }
  },

  associateTag: function(e, tag, selected) {
    var transaction_ids = [];
    var list = this.getTransactionList();
    e.removeCls('tag-some-associated');
    selected.forEach(function(record) {
      transaction_ids.push(record.get('id'));
    });
    list.fireEvent(
        'tagassociated',
        e.checked,
        tag.get('id'),
        transaction_ids);
  },

  deAssociate: function() {
    var transaction_ids = [];
    var list = this.getTransactionList();
    var model = list.getSelectionModel();
    model.selected.each(function(record) {
      transaction_ids.push(record.get('id'));
    });
    Ext.Ajax.request({
      method  : 'POST',
      jsonData: {
        transactions: transaction_ids
      },
      url     : '/api/transaction/deassociate',
      success : function (resp) {
        Ext.example.msg(
            'Removed tags',
            'Successfully removed all tags from transactions');
      }
    });
  },

  changeType: function(combo, records) {
    var type = combo.getValue();
    var win = this.getTransactionAdd();

    if (type == 1 || type == 2) {
      win.down('#combo-category').show();
      win.down('#combo-account').hide();
      win.down('#transaction-rate').disable();
      win.down('#transaction-final').disable();
      win.down('#transaction-tags').enable();
    } else if (type == 3) {
      win.down('#combo-category').hide();
      win.down('#combo-account').show();
      win.down('#transaction-tags').disable();

      var account_id = win.down('#combo-account').getValue();
      if (account_id != null && account_id != 0) {
        var accounts = this.getAccountStore();
        var account = accounts.getById(account_id);
        this.enableCurrency(account.get('currency'));
      }
    }
  },

  setCurrency: function(combo, records) {
    var currency = records[0].get('currency');
    this.enableCurrency(currency);
  },

  enableCurrency: function(currency) {
    var win = this.getTransactionAdd();
    var accounts = this.getAccountStore();
    var account = accounts.getById(this.selected_account);

    if (account.get('currency') != currency) {
      var rateField = win.down('#transaction-rate');
      rateField.enable();
      var finalField = win.down('#transaction-final');
      finalField.enable();
      this.setCurrencyRate(account.get('currency'), currency, rateField, finalField);
    } else {
      win.down('#transaction-rate').disable();
      win.down('#transaction-final').disable();
    }
  },

  setCurrencyRate: function(from, to, rateField, finalField) {
    var win = this.getTransactionAdd();

    Ext.Ajax.request({
      method : 'GET', 
      params : {
        from: from,
        to  : to
      },
      url    : '/fx/rate',
      success: function (resp) {
        if (!isNaN(resp.responseText)) {
          rateField.setValue(resp.responseText);
        } else {
          rateField.setValue(1);
        }
        finalField.setValue('');
      }
    });
  },

  saveTransaction: function() {
    var win = this.getTransactionAdd();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();
    record.set(values);
    record.tags().clearData();
    var tagStore = this.getTagStore();
    var transactionStore = this.getTransactionStore();
    var account = this.selected_account;
    var app = this.application;

    var tags = form.down('#transaction-tags').items.items;
    tags.forEach(function(tag_element) {
      if (tag_element.value) {
        var patt = /\d+/g;
        var id = parseInt(patt.exec(tag_element.name));
        var tag = tagStore.getById(id);
        tag.setDirty();
        record.tags().add(tag);
      }
    });
    record.set('account_from', account);

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          transactionStore.load({
            callback: function() {
              win.close();
              app.fireEvent('addtransaction', 'account', account);
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

  exportCsv: function() {
    var url = 'api/transaction/csv?type=' + this.type;
    if (this.type != 'wealth') {
      url += '&id=' + this.id;
    }
    window.open(url, '_blank');
  },

  upload: function() {
    Ext.widget('upload');
  },

  uploadTransactions: function() {
    var win = this.getUploadWindow();
    var form = win.down('form');
    var store = this.getTransactionStore();

    if (form.getForm().isValid()) {
      form.el.mask('Re-calculating splines..');
      form.submit({
        url    : '/api/transaction/upload/' + this.selected_account,
        success: function(rec, op) {
          store.load({
            callback: function() {
              win.close();
            }
          });
        },
        failure: function(rec, op) {
          form.el.unmask();
          var errors = op.result.errors;
          if (errors) {
            form.getForm().markInvalid(errors);
          } else {
            form.down('filefield').markInvalid(op.result.message);
          }
        },
      });
    }
  }
});
