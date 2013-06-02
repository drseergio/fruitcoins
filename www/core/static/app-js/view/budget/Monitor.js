Ext.require(['Ext.chart.*']);

Ext.define('moneypit.view.budget.Monitor', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.budgetmonitor',
  border       : false,
  layout       : 'fit',

  items        : {
    xtype: 'chart',
    store: 'BudgetLine',
    animate: true,
    style: 'background:#fff',
    shadow: false,
    axes: [{
        type: 'Numeric',
        position: 'bottom',
        fields: ['progress'],
        minimum: 0,
        maximum: 100,
        majorTickSteps: 5,
        grid: {
          even: {
            opacity: 1,
            fill: '#ddd',
            stroke: '#bbb',
            'stroke-width': 1
          }
        },
      }, {
        type: 'Category',
        position: 'left',
        fields: ['category'],
        hidden: true,
    }],
    series: [{
      type  : 'bar',
      axis  : 'bottom',
      highlight: true,
      xField: 'category',
      renderer: function(sprite, record, attr, index, store) {
        var progress = record.get('progress');
        var type = record.get('type');
        var color = 'rgb(44, 153, 201)';
        if (progress < 75) {
          if (type == 2) {
            color = 'rgb(49, 149, 0)';
          } else {
            color = 'rgb(213, 0, 49)';
          }
        } else if (progress < 100) {
          color = 'rgb(249, 153, 0)';
        } else if (progress >= 97) {
          if (type == 2) {
            color = 'rgb(213, 0, 49)';
          } else {
            color = 'rgb(49, 149, 0)';
          }
        }
        return Ext.apply(attr, {
          fill: color
        });
      },
      yField: 'progress',
      label: {
        display: 'insideStart',
        field: 'id',
        orientation: 'horizontal',
        color: '#333',
        font: '13px Helvetica, sans-serif',
        'text-anchor': 'middle',
        contrast: true
      }
    }]
  },

  initComponent: function() {
    this.callParent(arguments);
  },
})
