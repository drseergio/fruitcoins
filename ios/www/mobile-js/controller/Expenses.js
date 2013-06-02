Ext.regController('Expenses', {
  url: fruitcoinsUrl + 'api/report/expenses',
  store: 'Expenses',
  view: 'expenses',

  show: function(options) {
    if (!this.chartView) {
      this.chartView = this.render({
        xtype: this.view
      });
    }

    var store = Ext.getStore(this.store);
    store.proxy.extraParams = {
      date_from: this.getStringDate(options.dates.date_from),
      date_to: this.getStringDate(options.dates.date_to),
    };
    store.load();

    this.application.viewport.setActiveItem(this.chartView);
  },

  getStringDate: function(date) {
    return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
  }
});
