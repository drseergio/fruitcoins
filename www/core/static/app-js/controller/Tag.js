Ext.define('moneypit.controller.Tag', {
  extend: 'Ext.app.Controller',
  views : [ 'tag.Edit', 'tag.List' ],
  stores: [ 'Tag' ],
  models: [ 'Tag' ],

  refs: [{
      selector: 'taglist',
      ref     : 'tagList'
    }, {
      selector: 'tagedit',
      ref     : 'tagEdit'
  }],

  init            : function() {
    this.control({
      'taglist'             : {
        cellclick: this.openTransactions
      },
      'taglist actioncolumn': {
        click    : this.onActionColumn
      },
      'tagedit button[action=save]': {
        click: this.saveTag
      },
      'tagedit #tag-name': {
        afterrender: this.setFocus,
        specialkey: this.onAddKey
      },
      'taglist button[action=new]': {
        click: this.newTag
      }
    });

    this.application.on({
      loadtransactions : this.onLoadTransactions,
      scope            : this
    });
  },

  onLoadTransactions : function() {
    var list = this.getTagList();
    list.getSelectionModel().deselectAll();
  },

  onAddKey           : function(field, e) {
    if (e.getKey() == e.ENTER) {
      this.saveTag();
    }
  },

  onActionColumn  : function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var action = e.target.getAttribute('class');
    if (action.indexOf("x-action-col-0") != -1) {
      this.editTag(rec);
    } else if (action.indexOf("x-action-col-1") != -1) {
      this.deleteTag(rec);
    }
  },

  newTag: function() {
    this.editTag();
  },

  editTag: function(record) {
    var view = Ext.widget('tagedit');
    var form = view.down('form');
    if (record) {
      form.loadRecord(record);
    }
  },

  deleteTag: function(record) {
    var store = this.getTagStore();
    var app = this.application;
    Ext.MessageBox.confirm('Confirm', 'Are you sure you want to do that?', function(btn) {
      if (btn == 'yes') {
        var id = record.get('id');
        store.remove(record);
        app.fireEvent('deletetag', id);
      }
    });
  },

  saveTag: function() {
    var win = this.getTagEdit();
    var store = this.getTagStore();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();

    if (record) {
      record.unjoin(store);
    } else {
      record = Ext.create('moneypit.model.Tag');
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
              app.fireEvent('edittag', rec.get('id'));
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

  setFocus: function(field) {
    field.focus(false, 800);
  },

  openTransactions: function(iView, iCellEl, iColIdx, record, iRowEl, iRowIdx, iEvent) {
    var fieldName = iView.getGridColumns()[iColIdx].dataIndex;

    if (fieldName == 'name') {
      var transactionController = this.getController('Transaction');
      transactionController.openTag(record.get('id'));
    }
  },
});
