MoneypitMobile.views.NetIncome = Ext.extend(Ext.chart.Chart, {
  interactions: [{
    type: 'panzoom',
    axes: {
      left: {
        maxZoom: 2
      },
      bottom: {
        maxZoom: 4
      },
      right: {
        minZoom: 0.5,
        maxZoom: 4,
        allowPan: false
      }
    }
  }],
  animate: false,
  store: 'NetIncome',
  axes: [{
      type: 'Numeric',
      position: 'right',
      fields: ['amount'],
      grid: {
        odd: {
          opacity: 1,
          fill: '#ddd',
          stroke: '#bbb',
          'stroke-width': 0.5
        }
      }
    }, {
      type: 'Category',
      position: 'bottom',
      fields: ['month'],
  }],
  series: [{
    smooth: true,
    type: 'line',
    showMarkers: false,
    fill: true,
    axis: 'right',
    xField: 'month',
    yField: 'amount'
  }]
});
Ext.reg('netincome', MoneypitMobile.views.NetIncome);
