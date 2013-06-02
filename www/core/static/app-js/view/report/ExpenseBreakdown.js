Ext.define('moneypit.view.report.ExpenseBreakdown', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.categoryexpense',

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
          store: 'ExpenseBreakdown',
          shadow: true,
          style: 'background:#fff',
          legend: {
            position: 'right',
          },
          insertPadding: 60,
          series: [{
            type: 'pie',
            field: 'amount',
            tips: {
              trackMouse: true,
              width: 140,
              height: 40,
              renderer: function(record, item) {
                var store = record.store; 
                var total = 0;
                store.each(function(rec) {
                  total += rec.get('amount');
                });
                this.setTitle(
                    record.get('name') + ': ' +
                    record.get('amount').toFixed(2) + ' ' + 
                    wealthCurrency + ' ' +
                    Math.round(record.get('amount') / total * 100)+ '%');
              }
            },
            highlight: {
              segment: {
                margin: 20
              }
            },
            label: {
              field: 'name',
              display: 'rotate',
              contrast: true,
              font: '18px Droid Sans'
            }
          }]
        }]
      }, {
        region: 'center',
        border: false,
        layout: 'fit',
        items: [{
        border: false,
          xtype: 'grid',
          store: 'ExpenseBreakdown',
          columns: [{
              header      : 'Category',
              dataIndex   : 'full_name',
              flex        : 2,
              sortable    : true,
              menuDisabled: true,
            }, {
              header      : 'Amount',
              dataIndex   : 'amount',
              flex        : 1,
              sortable    : true,
              menuDisabled: true,
          }],
        }]
    }];

    this.callParent(arguments);
  }
});
