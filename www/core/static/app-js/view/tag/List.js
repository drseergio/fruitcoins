Ext.define('moneypit.view.tag.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.taglist',
  border       : false,
  cls          : 'sidebar-toolbar',
  initComponent: function() {
    this.store = 'Tag';
    this.stripeRows = true;
    this.hideHeaders = true;
    this.tbar = [{
        text    : 'New..',
        iconCls : 'icons-tag',
        action  : 'new'
    }];
    this.columns = [{
        flex     : 8,
        id       : 'tagColumn',
        dataIndex: 'name',
      }, {
        flex     : 3,
        xtype    : 'actioncolumn',
        items    : [{
            id  : 'icons-edit',
            icon: staticPath + '/resources/images/icons/edit.png',
          }, {
            id  : 'icons-delete',
            icon: staticPath + '/resources/images/icons/delete.png',
        }]
    }];
    this.callParent(arguments);
  },

  viewConfig: {
    emptyText: '<div class="emptyText">Put transactions into meaningful groupings with tags, drag\'n\'drop included!</div>',
    deferEmptyText: false,
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
