Ext.regController('Period', {
  reportmap: {
    '#report-networth': 'NetWorth',
    '#report-netincome': 'NetIncome',
    '#report-expenses': 'Expenses',
    '#report-incomes': 'Incomes',
    '#report-expense-bd': 'ExpenseBreakdown',
    '#report-income-bd': 'ExpenseBreakdown',
  },
  index: function(options) {
    if (!this.periodView) {
      this.periodView = this.render({
        xtype: 'period',
      });
      var me = this;
      this.periodView.query('#run-report')[0].setHandler(function() {
        me.report();
      });
    }
 
    this.application.viewport.setActiveItem(this.periodView);
  },
  report: function() {
    var me = this;
    var values = this.periodView.getValues();
    var isInvalid = this.isinvalid(values);
    if (!isInvalid) {
      Ext.dispatch({
        dates: values,
        controller: values.report_type,
        action: 'show',
        historyUrl: 'Period/index',
        animation: {
          type: 'slide',
          reverse: true
        }
      });
    } else {
      Ext.Msg.alert('Invalid period', isInvalid, Ext.emptyFn);
    }
  },
  isinvalid: function(values) {
    var date_from = values.date_from;
    var date_to = values.date_to;
    var report_type = values.report_type;
    var now = new Date();

    if (report_type != 'ExpenseBreakdown' && report_type != 'IncomeBreakdown') {
      if (date_from.getFullYear() == date_to.getFullYear() &&
          date_from.getMonth() == date_to.getMonth()) {
        return 'Must choose different months';
      }
    }

    if (this.isfuture(date_from, now)) {
      return 'Not yet capable of prediction';
    }
    if (this.isfuture(date_from, date_to)) {
      return '"From" must be before "To"';
    }
    return false;
  },
  isfuture: function(then, now) {
    if (then.getFullYear() > now.getFullYear() ||
        (then.getFullYear() == now.getFullYear() && then.getMonth() > now.getMonth()) ||
        (then.getFullYear() == now.getFullYear() && then.getMonth() == now.getMonth() && then.getDate() > now.getDate())) {
      return true;
    }
  }
});
