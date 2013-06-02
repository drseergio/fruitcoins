MoneypitMobile.views.NetWorth = Ext.extend(Ext.chart.Chart, {
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
  store: 'NetWorth',
  axes: [{
      type: 'Numeric',
      position: 'right',
      fields: ['balance'],
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
    yField: 'balance'
  }]
});
Ext.reg('networth', MoneypitMobile.views.NetWorth);
