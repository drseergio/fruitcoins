MoneypitMobile.views.ExpenseBreakdown = Ext.extend(Ext.chart.Panel, {
  items: {
    theme: 'Demo',
    animate: true,
    insetPadding: 20,
    legend: {
      position: {
        portrait: 'bottom',
        landscape: 'left'
      }
    },
    store: 'ExpenseBreakdown',
    interactions: [{
        type: 'reset',
        confirm: true
      }, {
        type: 'rotate'
      }, {
        type: 'iteminfo',
        gesture: 'taphold',
        listeners: {
          show: function(interaction, item, panel) {
            var storeItem = item.storeItem;
            panel.update(['<ul><li><b>Category: </b>' + storeItem.get('name') + '</li>', '<li><b>Value: </b> ' + storeItem.get('amount') + '</li></ul>'].join(''));
          }
        }
      }, {
        type: 'piegrouping',
        onSelectionChange: function(me, items) {
          var chartPanel = me.ownerCt.ownerCt;
          if (items.length) {
            var sum = 0,
            i = items.length;
            while(i--) {
              sum += items[i].storeItem.get('amount');
            }
            chartPanel.descriptionPanel.setTitle('Total: ' + sum);
            chartPanel.headerPanel.setActiveItem(1, {
              type: 'slide',
              direction: 'left'
            });
          } else {
            chartPanel.headerPanel.setActiveItem(0, {
              type: 'slide',
              direction: 'right'
            });
          }
        }
    }],
    series: [{
      type: 'pie',
      field: 'amount',
      showInLegend: true,
      highlight: false,
      listeners: {
        'labelOverflow': function(label, item) {
          item.useCallout = true;
        }
      },
      callouts: {
        renderer: function(callout, storeItem) {
          callout.label.setAttributes({
            text: storeItem.get('name')
          }, true);
        },
        filter: function() {
          return false;
        },
        box: {
          //no config here.
        },
        lines: {
          'stroke-width': 2,
           offsetFromViz: 20
        },
        label: {
          font: 'italic 14px Arial'
        },
        styles: {
          font: '14px Arial'
        }
      },
      label: {
        field: 'name',
        display: 'rotate',
        contrast: true,
        font: '18px Arial'
      }
    }]
  }
});
Ext.reg('categoryexpense', MoneypitMobile.views.ExpenseBreakdown);
