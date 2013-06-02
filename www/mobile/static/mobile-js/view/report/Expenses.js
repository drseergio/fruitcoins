MoneypitMobile.views.Expenses = Ext.extend(Ext.chart.Chart, {
  gradients: [{
    'id'   : 'v-1',
    'angle': 0,
    stops  : {
      0: { color: 'rgb(212, 40, 40)' },
      100: { color: 'rgb(117, 14, 14)' }
    }
  }],
  theme: 'Demo',
  cls: 'column1',
  animate: true,
  store: 'Expenses',
  axes: [{
      type: 'Numeric',
      position: 'left',
      minimum: 0,
      fields: ['amount'],
      label: {
        renderer: function(v) {
          return v.toFixed(0);
        }
      },
    }, {
      type: 'Category',
      position: 'bottom',
      fields: ['month'],
  }],
  series: [{
    renderer: function(sprite, storeItem, barAttr, i, store) {
      barAttr.fill = 'url(#v-1)';
      return barAttr;
    },
    label: {
      orientation: 'vertical',
      field: 'amount'
    },
    type: 'column',
    highlight: true,
    axis: 'left',
    xField: 'month',
    yField: 'amount',
  }]
});
Ext.reg('expenses', MoneypitMobile.views.Expenses);
