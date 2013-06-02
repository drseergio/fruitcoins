Ext.define('moneypit.view.account.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.accountlist',
  border       : false,
  cls          : 'sidebar-toolbar',
  initComponent: function() {
    this.store = 'Account';
    this.hideHeaders = true;
    this.tbar = [{
        text    : 'New..',
        iconCls : 'icons-add',
        action  : 'new'
      }, {
        text    : 'Home',
        action  : 'showwealth',
        iconCls : 'icons-house'
    }];
    this.columns = [{
        flex     : 6,
        id       : 'accountColumn',
        dataIndex: 'name',
        renderer : function(value, metaData, record) {
          var type = '';
          if (record.get('type') == 1) {
            type = 'Saving';
          } else if (record.get('type') == 2) {
            type = 'Checking';
          } else if (record.get('type') == 3) {
            type = 'Cash';
          } else if (record.get('type') == 4) {
            type = 'Credit card';
          } else if (record.get('type') == 6) {
            type = 'Generic asset';
          }
          return '<div style="font-family: \'Droid Sans\'; font-size: 1.1em; font-weight: 600">' + value + '</div>' +
            '<div style="font-weight: normal; font-size: 12px!important; float: left">' +
            type + ', ' + record.get('currency') + '</div>' +
            '<div style="float: right; font-weight: normal; font-size: 12px!important;">' +
            '</div>';
        }
      }, {
        flex     : 2,
        xtype    : 'actioncolumn',
        items    : [{
            id  : 'account-edit',
            icon: staticPath + '/resources/images/icons/edit.png',
          }, {
            id  : 'account-delete',
            icon: staticPath + '/resources/images/icons/delete.png',
        }]
    }];
    this.plugins = [
        Ext.create('Ext.ux.RowDropZone'),
    ];
    this.callParent(arguments);
  },

  viewConfig: {
    emptyText: '<div class="emptyText">You currently don\'t have any accounts :(, click <b>New</b> to create some</div>',
    listeners: {
      render: function(v) {
        v.dragZone = Ext.create('Ext.dd.DragZone', v.getEl(), {
          getDragData: function(e) {
            var sourceEl = e.getTarget(v.itemSelector, 10), d;
            if (sourceEl) {
              d = sourceEl.cloneNode(true);
              d.id = Ext.id();
              return v.dragData = {
                sourceEl: sourceEl,
                repairXY: Ext.fly(sourceEl).getXY(),
                ddel    : d,
                store   : v.store,
                record  : v.getRecord(sourceEl)
              };
            }
          },
          getRepairXY: function() {
            return this.dragData.repairXY;
          }
        });
      }
    }
  }
});
