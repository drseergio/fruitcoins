Ext.define('moneypit.controller.Report', {
  extend          : 'Ext.app.Controller',
  views           : [
      'report.Expenses',
      'report.ExpenseBreakdown',
      'report.Incomes',
      'report.IncomeBreakdown',
      'report.NetWorth',
      'report.Report' ],
  stores          : [ 'ReportType' ],

  refs: [{
      selector: 'reports',
      ref     : 'reportPanel'
  }],

  init            : function() {
    this.control({
      'reports button[action=import]': {
      },
      'reports combo': {
        change: this.onReportChange
      },
      'reports #report-from': {
        change: this.enableRun
      },
      'reports #report-to': {
        change: this.enableRun
      },
      'reports button[action=show]': {
        click: this.loadReport
      },
      'reports button[action=close]': {
        click: this.closeReport
      }
    });

    this.application.on({
      scope            : this
    });
  },

  onReportChange: function(combo, newValue, oldValue) {
    this.enableRun();
  },

  enableRun: function() {
    var reportPanel = this.getReportPanel();
    var typeCombo = reportPanel.down('combo'); 
    var dateFrom = reportPanel.down('#report-from').getValue();
    var dateTo = reportPanel.down('#report-to').getValue();
    if (typeCombo.getValue() != null &&
        typeCombo.getValue() != '' &&
        this.isValidPeriod(dateFrom, dateTo)) {
      reportPanel.down('button[action=show]').enable();
    } else {
      reportPanel.down('button[action=show]').disable();
    }
  },

  isValidPeriod: function(dateFrom, dateTo) {
    if (!dateFrom || !dateTo) {
      return false;
    }
    if (dateTo < dateFrom) {
      return false;
    }
    if (dateFrom > new Date()) {
      return false;
    }
    return true;
  },

  loadReport: function() {
    var reportPanel = this.getReportPanel();
    reportPanel.removeAll();
    var chartType = reportPanel.down('combo').getValue();
    if (chartType == 1) {
      reportPanel.add(Ext.widget('networth'));
    } else if (chartType == 2) {
      reportPanel.add(Ext.widget('expenses'));
    } else if (chartType == 3) {
      reportPanel.add(Ext.widget('incomes'));
    } else if (chartType == 4) {
      reportPanel.add(Ext.widget('netincome'));
    } else if (chartType == 5) {
      reportPanel.add(Ext.widget('categoryexpense'));
    } else if (chartType == 6) {
      reportPanel.add(Ext.widget('categoryincome'));
    }
    reportPanel.down('button[action=close]').enable();
  },

  closeReport: function() {
    var reportPanel = this.getReportPanel();
    reportPanel.removeAll();
    reportPanel.down('button[action=close]').disable();
  }
});
