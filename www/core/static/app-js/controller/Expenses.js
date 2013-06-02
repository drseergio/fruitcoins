Ext.define('moneypit.controller.Expenses', {
  extend          : 'Ext.app.Controller',
  views           : [
      'report.Expenses',
      'report.Report' ],
  stores          : [ 'Expenses' ],
  models          : [ 'Expenses' ],

  refs: [{
      selector: 'reports',
      ref     : 'reportPanel'
  }],

  init            : function() {
    this.control({
      'expenses' : {
        render: this.onRender
      }
    });

    this.application.on({
      scope            : this
    });
  },

  onRender: function() {
    var reportPanel = this.getReportPanel();
    var fieldFrom = reportPanel.down('#report-from');
    var dateFrom = fieldFrom.getValue();
    var dateTo = reportPanel.down('#report-to').getValue();
    var store = this.getExpensesStore();
    var me = this;
    store.getProxy().extraParams = {
      date_from: me.getStringDate(dateFrom),
      date_to: me.getStringDate(dateTo)
    };
    reportPanel.el.mask('Guessing with education..');
    store.load({
      callback: function(records, operation, success) {
        reportPanel.el.unmask();
        fieldFrom.markInvalid(operation.request.scope.reader.jsonData.message);
        if (!success) {
          reportPanel.removeAll();
        }
      }
    });
  },

  getStringDate: function(date) {
    return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
  }
});
