MoneypitMobile.views.Incomes = Ext.extend(Ext.chart.Chart, {
  gradients: [{
    'id'   : 'v-1',
    'angle': 0,
    stops  : {
      0: { color: 'rgb(180, 216, 42)' },
      100: { color: 'rgb(94, 114, 13)' }
    }
  }],
  theme: 'Demo',
  cls: 'column1',
  animate: true,
  store: 'Incomes',
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
Ext.reg('incomes', MoneypitMobile.views.Incomes);
