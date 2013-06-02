Ext.define('moneypit.controller.Liberation', {
  extend          : 'Ext.app.Controller',
  views           : [
      'liberation.Import',
      'liberation.List',
      'liberation.Summary' ],
  stores          : [ 'Import' ],
  models          : [ 'Import' ],

  refs: [{
      selector: 'liberation',
      ref     : 'liberationList'
    }, {
      selector: 'import',
      ref     : 'importWindow'
  }],

  init            : function() {
    this.control({
      'liberation button[action=import]': {
        click: function() {
          this.importData();
        }
      },
      'import button[action=upload]': {
        click: function() {
          this.uploadFile();
        } 
      },
      'liberation button[action=discard]': {
        click: function() {
          this.discardImport();
        }
      },
      'liberation button[action=commit]': {
        click: function() {
          this.commitImport();
        }
      }
    });

    this.application.on({
      scope            : this
    });

    this.getImportStore().addListener('load', this.onImportLoad, this);
  },

  onImportLoad: function(store) {
    var list = this.getLiberationList();
    if (store.getCount() > 0) {
      list.down('button[action=import]').disable();
      list.down('button[action=commit]').enable();
      list.down('button[action=discard]').enable();
    } else {
      list.down('button[action=import]').enable();
      list.down('button[action=commit]').disable();
      list.down('button[action=discard]').disable();
    }
  },

  importData: function() {
    var view = Ext.widget('import');
  },

  uploadFile: function() {
    var win = this.getImportWindow();
    var form = win.down('form');
    var store = this.getImportStore();

    if (form.getForm().isValid()) {
      form.el.mask('Reticulating splines..');
      form.submit({
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
  },

  discardImport: function() {
    var store = this.getImportStore();
    Ext.Ajax.request({
      method  : 'POST',
      url     : '/api/liberation/discard',
      success : function (resp) {
        Ext.example.msg(
            'Discard',
            'All imported data has been discarded');
        store.load();
      }
    });
  },

  commitImport: function() {
    var me = this;
    Ext.MessageBox.wait('Calculating life expectancy.. Please wait');

    Ext.Ajax.request({
      method  : 'POST',
      url     : '/api/liberation/commit',
      success : function (resp) {
        setTimeout(function() {
          me.waitProgress(me);
        }, 5000);
      },
      failure : function() {
        Ext.MessageBox.hide();
      }
    });
  },

  waitProgress: function(me) {
    Ext.Ajax.request({
      method  : 'POST',
      url     : '/api/liberation/progress',
      success : function (resp) {
        var result = Ext.decode(resp.responseText);
        if (result.success) {
          Ext.MessageBox.hide();
          me.getController('Account').getAccountStore().load();
          Ext.example.msg(
              'All done',
              'Successfully imported valuable data');
          me.getImportStore().load();
        } else {
          setTimeout(function() {
            me.waitProgress(me);
          }, 3000);
        }
      },
    });
  }
});
