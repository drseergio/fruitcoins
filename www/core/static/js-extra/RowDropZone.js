Ext.require([
  "Ext.dd.DropZone"], function() {
    Ext.define('Ext.ux.RowDropZone', {
      extend: 'Ext.dd.DropZone',

      constructor: function(){},

      init: function(grid) {
        var me = this;

        if (grid.rendered) {
          me.grid = grid;
          grid.getView().on({
            render: function(v) {
              me.view = v;
              Ext.ux.RowDropZone.superclass.constructor.call(me, me.view.el);
            },
            single: true
          });
        } else {
          grid.on('render', me.init, me, {single: true});
        }
      },

      containerScroll: true,

      getTargetFromEvent: function(e) {
        var me = this,
            v = me.view;

        var cell = e.getTarget(v.cellSelector);
        if (cell) {
          var row = v.findItemByChild(cell);
          if (row) {
            return {
              node  : cell,
              record: v.getRecord(row),
            };
          }
        }
      },

      onNodeEnter: function(target, dd, e, dragData) {
        delete this.dropOK;

        var isSourceAccount = dragData.record instanceof moneypit.model.Account;
        var isSourceTag = dragData.record instanceof moneypit.model.Tag;

        if (!target) {
          return;
        }
        var isTargetTransaction = target.record instanceof moneypit.model.Transaction;
        var isTargetAccount = target.record instanceof moneypit.model.Account;

        if ((isSourceAccount && isTargetAccount && target.record != dragData.record) ||
            (isSourceTag && isTargetTransaction && target.record.get('type') != 3)) {
          this.dropOK = true;
          Ext.fly(target.node).addCls('x-drop-target-active');
        }
      },

      onNodeOver: function(target, dd, e, dragData) {
        return this.dropOK ? this.dropAllowed : this.dropNotAllowed;
      },

      onNodeOut: function(target, dd, e, dragData) {
        Ext.fly(target.node).removeCls('x-drop-target-active');
      },

      onNodeDrop: function(target, dd, e, dragData) {
        var isSourceAccount = dragData.record instanceof moneypit.model.Account;
        var isSourceTag = dragData.record instanceof moneypit.model.Tag;

        var isTargetTransaction = target.record instanceof moneypit.model.Transaction;
        var isTargetAccount = target.record instanceof moneypit.model.Account;

        if (this.dropOK) {
          if (isSourceTag && isTargetTransaction) {
            this.grid.fireEvent(
                'tagassociated',
                true,
                dragData.record.get('id'),
                [target.record.get('id')]);
            return true;
          }
          if (isSourceAccount && isTargetAccount) {
            this.grid.fireEvent(
                'newtransfer',
                dragData.record.get('id'),
                target.record.get('id'));
            return true;
         }
        }
      }
  });
});
