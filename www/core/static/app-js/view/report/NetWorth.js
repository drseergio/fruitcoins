Ext.define('moneypit.view.report.NetWorth', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.networth',

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
          store: 'NetWorth',
          axes: [{
              type: 'Numeric',
              position: 'right',
              fields: ['balance'],
              label: {
                 renderer: Ext.util.Format.numberRenderer('0,0')
              },
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
              highlight: {
                size: 7,
                radius: 7
              },
              tips: {
                trackMouse: true,
                width: 140,
                height: 28,
                renderer: function(record, item) {
                  this.setTitle(
                      record.get('month') + ': ' +
                      record.get('balance').toFixed(2) + ' ' + 
                      wealthCurrency);
                }
              },
              type: 'line',
              axis: 'left',
              smooth: true,
              fill  : true,
              xField: 'month',
              yField: ['balance'],
          }]
        }]
      }, {
        region: 'center',
        border: false,
        layout: 'fit',
        items: [{
        border: false,
          xtype: 'grid',
          store: 'NetWorth',
          columns: [{
              header      : 'Month',
              dataIndex   : 'month',
              flex        : 2,
              sortable    : false,
              menuDisabled: true,
            }, {
              header      : 'Balance',
              dataIndex   : 'balance',
              flex        : 1,
              sortable    : false,
              menuDisabled: true,
          }],
        }]
    }];

    this.callParent(arguments);
  }
});
