Ext.define('moneypit.view.report.NetIncome', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.netincome',

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
          store: 'NetIncome',
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
                      record.get('amount').toFixed(2) + ' ' + 
                      wealthCurrency);
                }
              },
              type: 'line',
              axis: 'left',
              smooth: true,
              fill  : true,
              xField: 'month',
              yField: ['amount'],
          }]
        }]
      }, {
        region: 'center',
        border: false,
        layout: 'fit',
        items: [{
        border: false,
          xtype: 'grid',
          store: 'NetIncome',
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
