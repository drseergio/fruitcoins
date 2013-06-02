Ext.define('moneypit.view.report.Expenses', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.expenses',

  initComponent: function() {
    this.layout       = 'border';
    this.items        = [{
        region: 'north',
        frame : false,
        border: false,
        layout: 'fit',
        height: 400,
        items: [{
          xtype: 'chart',
          animate: true,
          style: 'background:#fff',
          shadow: true,
          store: 'Expenses',
          gradients: [{
            'id'   : 'v-1',
            'angle': 0,
            stops  : {
              0: { color: 'rgb(212, 40, 40)' },
              100: { color: 'rgb(117, 14, 14)' }
            }
          }],
          axes: [{
              type: 'Numeric',
              position: 'right',
              fields: ['amount'],
              label: {
                 renderer: Ext.util.Format.numberRenderer('0,0')
              },
              grid: {
                odd: {
                  opacity: 1,
                  fill: '#ddd',
                  stroke: '#bbb',
                  'stroke-width': 1
                }
              },
            }, {
              type: 'Category',
              position: 'bottom',
              fields: ['month'],
            }],
          series: [{
             label: {
                display: 'insideStart',
                field: 'amount',
                orientation: 'vertical',
                contrast: true,
                font: '16px Droid Sans',
                'text-anchor': 'middle'
              },
              renderer: function(sprite, storeItem, barAttr, i, store) {
                  barAttr.fill = 'url(#v-1)';
                  return barAttr;
              },
              highlight: true,
              type: 'column',
              axis: 'left',
              xField: 'month',
              yField: 'amount',
          }]
        }]
      }, {
        region: 'center',
        border: false,
        layout: 'fit',
        items: [{
        border: false,
          xtype: 'grid',
          store: 'Expenses',
          columns: [{
              header      : 'Month',
              dataIndex   : 'month',
              flex        : 2,
              sortable    : false,
              menuDisabled: true,
            }, {
              header      : 'Amount',
              dataIndex   : 'amount',
              flex        : 1,
              sortable    : false,
              menuDisabled: true,
          }],
        }]
    }];

    this.callParent(arguments);
  }
});
