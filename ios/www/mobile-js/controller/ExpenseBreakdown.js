Ext.regController('ExpenseBreakdown', {
  url: fruitcoinsUrl + 'api/report/category/expense',
  store: 'ExpenseBreakdown',
  view: 'categoryexpense',

  show: function(options) {
    var store = Ext.getStore(this.store);
    store.proxy.extraParams = {
      date_from: this.getStringDate(options.dates.date_from),
      date_to: this.getStringDate(options.dates.date_to),
    };

    if (!this.chartView) {
      var me = this;
      store.load(function() {
        me.chartView = me.render({
          xtype: me.view
        });
        me.application.viewport.setActiveItem(me.chartView);
      });
    } else {
      store.load();
      this.application.viewport.setActiveItem(this.chartView);
    }
  },

  getStringDate: function(date) {
    return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
  }
});
