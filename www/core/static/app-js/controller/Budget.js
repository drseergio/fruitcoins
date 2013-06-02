Ext.define('moneypit.controller.Budget', {
  extend          : 'Ext.app.Controller',
  views           : [
      'budget.Edit',
      'budget.List',
      'budget.Monitor',
      'budget.Summary' ],
  stores          : [
      'Budget',
      'BudgetLine',
      'Category',
      'CategorySearch',
      'Import',
      'Period' ],
  models          : [ 'Budget', 'BudgetLine', 'Import' ],

  refs: [{
      selector: 'budgetlist',
      ref     : 'budgetList'
    }, {
      selector: 'budgetedit',
      ref     : 'budgetEdit'
    }, {
      selector: 'budgetmonitor',
      ref     : 'budgetMonitor'
    }, {
      selector: 'budgetsummary',
      ref     : 'budgetSummary'
  }],

  init            : function() {
    this.control({
      'budgetlist': {
        beforeedit: this.onBeforeEditBudgetLine,
        edit: this.onEditBudgetLine,
        render: this.onRender,
        selectionchange: this.onSelectionChange,
      },
      'budgetlist button[action=new]': {
        click: this.newBudget
      },
      'budgetlist #budget-combo': {
        change: this.onBudgetChange,
      },
      'budgetlist button[action=delete]': {
        click: function() {
          this.deleteBudget();
        }
      },
      'budgetlist button[action=new-line]': {
        click: function() {
          this.newLine();
        }
      },
      'budgetlist button[action=refresh]': {
        click: function() {
          this.getBudgetLineStore().load();
        }
      },
      'budgetedit button[action=save]': {
        click: function() {
          this.saveBudget();
        }
      },
      'budgetlist button[action=delete-line]': {
        click: this.deleteBudgetLine
      },
      'budgetedit #budget-name': {
        afterrender: this.setFocus,
        specialkey: this.onAddKey
      },
      'budgetedit #budget-year': {
        specialkey: this.onAddKey
      },
      'budgetmonitor chart': {
        render: this.onMonitorRender
      },
    });

    this.application.on({
      deletebudget     : this.onDeleteBudget,
      deletebudgetline : this.onDeleteBudgetLine,
      newbudget        : this.onNewBudget,
      editbudgetline   : this.onAfterEditBudgetLine,
      scope            : this
    });

    this.getBudgetStore().addListener('load', this.onBudgetLoad, this);
  },

  onAddKey           : function(field, e) {
    if (e.getKey() == e.ENTER) {
      this.saveBudget();
    }
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=period]');
    var periodStore = this.getPeriodStore();
    column.renderer = function(val) {
      var period = periodStore.getAt(val - 1);
      if (period) {
        return period.data.text;
      } else {
        return '';
      }
    };
    column = list.down('[dataIndex=amount]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=total_amount]');
    column.renderer = this.amountRenderer;
  },

  onMonitorRender: function(chart) {
    var store = this.getBudgetLineStore();
    chart.series.items[0].label.renderer = function(id) {
      var record = store.getById(id);
      return record.get('category') + ' ' + record.get('progress') + '%';
    };
  },

  onBudgetLoad: function(store) {
    var combo = this.getBudgetList().down('#budget-combo');
    var me = this;
    if (store.getCount() > 0) {
      var record = store.first();
      combo.enable();
      combo.setValue(record);
    }
  },

  onBudgetChange: function(combo, newValue, oldValue) {
    var store = this.getBudgetLineStore();
    var deleteButton = this.getBudgetList().down('#tbar-budget-delete');
    var newlineButton = this.getBudgetList().down('#tbar-budget-new-line');
    var refreshButton = this.getBudgetList().down('button[action=refresh]');
    if (newValue != null && newValue != '') {
      deleteButton.enable();
      newlineButton.enable();
      refreshButton.enable();
      var me = this;
      var summary = this.getBudgetSummary();
      if (!summary.rendered) {
        this.getBudgetSummary().addListener('render', function() {
          me.updateSummary(newValue);
        });
      } else {
        me.updateSummary(newValue);
      }
      store.removeAll();
      store.getProxy().extraParams = { budget: newValue };
      store.load({
        callback: function() {
          me.toggleMonitor();
        }
      });
    } else {
      deleteButton.disable();
      newlineButton.disable();
      refreshButton.disable();
    }
  },

  onNewBudget: function() {
    this.getBudgetStore().sync();
  },

  onDeleteBudget: function() {
    var combo = this.getBudgetList().down('#budget-combo');

    var list = this.getBudgetList();
    var linesStore = this.getBudgetLineStore();
    combo.setValue('');
    list.down('#tbar-budget-delete').disable();
    var store = this.getBudgetStore();
    if (store.getCount() == 0) {
      combo.disable();
    } 
    linesStore.removeAll();
    this.updateSummary();
    Ext.example.msg(
        'Deleted',
        'Successfully deleted budget');
  },

  onDeleteBudgetLine: function() {
    this.toggleMonitor();
  },

  onBeforeEditBudgetLine: function(e) {
    var form = e.grid.getPlugin('rowEditing').editor.form;
    var field = form.findField('category_id');
    var category_id = e.record.get('category_id');
    this.getCategorySearchStore().load();
    field.setValue(category_id);
  },

  onEditBudgetLine: function(editor, e) {
    var store = this.getBudgetLineStore();
    var me = this;
    store.mySync({
      callback: function() {
        store.load({
          callback: function() {
            me.application.fireEvent('editbudgetline');
          }
        });
      }
    });
  },

  onAfterEditBudgetLine: function(budget) {
    this.toggleMonitor();
  },

  onSelectionChange: function(model, record, index) {
    var win = this.getBudgetList();
    var del = win.down('button[action=delete-line]');

    if (model.hasSelection()) {
      del.enable();
    } else {
      del.disable();
    }
  },

  newBudget: function() {
    this.editBudget();
  },

  editBudget: function() {
    var view = Ext.widget('budgetedit');
  },

  saveBudget: function() {
    var win = this.getBudgetEdit();
    var store = this.getBudgetStore();
    var form = win.down('form');
    var values = form.getValues();
    var record = Ext.create('moneypit.model.Budget');
    record.set(values);
    var app = this.application;

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          store.load({
            callback: function() {
              win.close();
              app.fireEvent('newbudget');
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

  deleteBudget: function() {
    var combo = this.getBudgetList().down('#budget-combo');
    var store = this.getBudgetStore();
    var app = this.application;
    Ext.MessageBox.confirm('Confirm', 'Are you sure you want to do that?', function(btn) {
      if (btn == 'yes') {
        var id = combo.getValue();
        store.remove(store.getById(id));
        store.sync();
        app.fireEvent('deletebudget', id);
      }
    });
  },

  deleteBudgetLine: function() {
    var list = this.getBudgetList();
    var store = this.getBudgetLineStore();
    var model = list.getSelectionModel();
    model.selected.each(function(item) {
      store.remove(item);
    });
    store.mySync({
      scope   : this,
      callback: function() {
        this.application.fireEvent('deletebudgetline');
      }
    });
  },

  setFocus: function(field) {
    field.focus(false, 800);
  },

  updateSummary    : function(id) {
    var panel = this.getBudgetSummary();
    var me = this;

    if (id != null && id != '') {
      var Model = Ext.ModelManager.getModel('moneypit.model.Budget');

      Model.load(id, {
        success: function(obj) {
          obj.update_summary(panel);
        }
      });
    } else {
      panel.update('<div class="summary-header">&nbsp;</div><div class="summary-inside">No budget is currently loaded, click <b>Create</b> to create one</div>');
    }
  },

  amountRenderer: function(value, metaData, record) {
    if (record.get('type') == 1) {
      return '<span style="color:green;">' + value.toFixed(2) + '</span>';
    } else {
      return '<span style="color:red;">' + value.toFixed(2) + '</span>';
    }
  },

  toggleMonitor: function() {
    var store = this.getBudgetLineStore();
    var tab = Ext.ComponentQuery.query("#app-west-budget")[0];

    if (store.getCount() > 6) {
      tab.enable();
    } else {
      tab.disable();
      tab.collapse(true);
    }
  },

  newLine: function() {
    var list = this.getBudgetList();
    var rowEditing = list.getPlugin('rowEditing');
    var record = Ext.create('moneypit.model.BudgetLine');
    var store = this.getBudgetLineStore();

    rowEditing.cancelEdit();
    store.insert(0, record);
    rowEditing.startEdit(0, 0);
  }
});
