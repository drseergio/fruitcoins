Ext.define('moneypit.view.transaction.Summary', {
  extend       : 'Ext.Panel',
  alias        : 'widget.summarypanel',

  height       : 65,
  cls          : 'summary',
  border: false,
frame: false,

  initComponent: function() {
    this.callParent(arguments);
  }
});
