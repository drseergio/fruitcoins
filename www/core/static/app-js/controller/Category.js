Ext.define('moneypit.controller.Category', {
  extend          : 'Ext.app.Controller',
  views           : [ 'category.Edit', 'category.Tree' ],
  stores          : [ 'Category' ],
  models          : [ 'Category' ],

  init            : function() {
    this.control({
      'categorytree': {
        beforeitemdblclick: this.openTransactions,
        selectionchange   : this.onSelectionChange,
        beforeitemmove    : this.onBeforeItemMove
      },
      'categorytree button[action=new]': {
        click             : this.newCategory
      },
      'categorytree button[action=edit]': {
        click: this.editCategory
      },
      'categorytree button[action=delete]': {
        click: this.deleteCategory
      },
      'categorytree button[action=refresh]': {
        click: function() {
          this.getCategoryStore().load();
        }
      },
      'categoryedit #category-name': {
        afterrender: this.setFocus,
        specialkey: this.onAddKey
      },
      'categoryedit #category-description': {
        specialkey: this.onAddKey
      },
      'categoryedit button[action=save]': {
        click: this.saveCategory
      },
    });

    this.application.on({
      addtransaction   : this.onAddTransaction,
      deletetransaction: this.onDeleteTransaction,
      deletecategory   : this.onDeleteCategory,
      scope            : this
    });
  },

  refs: [{
      selector: 'categorytree',
      ref     : 'categoryTree'
    }, {
      selector: 'categoryedit',
      ref     : 'categoryEdit'
  }],

  onAddTransaction   : function(account) {
  },

  onDeleteTransaction: function(account) {
  },

  onDeleteCategory: function() {
    var tree = this.getCategoryTree();
    tree.getSelectionModel().deselectAll();
  },

  onSelectionChange: function(model, selected) {
    var win = this.getCategoryTree();
    var record = selected[0];
    if (model.hasSelection()) {
      if (record.get('id') != 'inc' && record.get('id') != 'exp') {
        win.down('#category-delete').enable();
        win.down('#category-rename').enable();
      } else {
        win.down('#category-delete').disable();
        win.down('#category-rename').disable();
      }
      win.down('#category-new').enable();
    } else {
      win.down('#category-delete').disable();
      win.down('#category-rename').disable();
      win.down('#category-new').disable();
    }
  },

  onAddKey           : function(field, e) {
    if (e.getKey() == e.ENTER) {
      this.saveCategory();
    }
  },

  onBeforeItemMove: function(node, oldParent, newParent) {
    if (node.get('id') == 'inc' || node.get('id') == 'exp') {
      return false;
    }
    if (newParent.get('id') == 'root') {
      return false;
    }
    var store = this.getCategoryStore();

    Ext.Ajax.request({
      method  : 'POST',
      jsonData: {
        id        : node.get('id'),
        new_parent: newParent.get('id'),
        old_parent: oldParent.get('id'),
      },
      url     : '/api/category/move',
      failure : function(resp) {
        store.load();
      }
    });
  },

  openTransactions: function(tree, record) {
    var id = record.get('id');
    if (id != 'exp' && id != 'inc') {
      var transactionController = this.getController('Transaction');
      transactionController.openCategory(id);      
    }
    return false;
  },

  newCategory: function() {
    var view = Ext.widget('categoryedit');
  },

  editCategory: function(record) {
    var view = Ext.widget('categoryedit');
    var form = view.down('form');
    var tree = this.getCategoryTree();
    var model = tree.getSelectionModel();
    var selected = model.getSelection()[0];
    form.loadRecord(selected);
  },

  deleteCategory: function() {
    var store = this.getCategoryStore();
    var tree = this.getCategoryTree();
    var model = tree.getSelectionModel();
    var record = model.getSelection()[0];
    var app = this.application;
    Ext.MessageBox.confirm('Confirm', 'All associated ransactions will be DELETED. Are you sure you want to do that?', function(btn) {
      if (btn == 'yes') {
        var id = record.get('id');
        store.getNodeById(id).destroy({
          callback: function() {
            app.fireEvent('deletecategory', id);
          }
        });
      }
    });
  },

  setFocus: function(field) {
    field.focus(false, 800);
  },

  saveCategory: function() {
    var win = this.getCategoryEdit();
    var store = this.getCategoryStore();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();

    if (record) {
      record.unjoin(store);
    } else {
      record = Ext.create('moneypit.model.Category');
      var tree = this.getCategoryTree();
      var model = tree.getSelectionModel();
      var selected = model.getSelection()[0];
      record.set('parent', selected.get('id'));
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
              app.fireEvent('editcategory', rec.get('id'));
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
  }
});
