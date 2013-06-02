Ext.define('moneypit.view.budget.Summary', {
  extend       : 'Ext.Panel',
  alias        : 'widget.budgetsummary',
  border       : false,

  height       : 65,
  html         : '<div class="summary-header">&nbsp;</div><div class="summary-inside">No budget is currently loaded, click <b>Create</b> to create one</div>',
  cls          : 'summary',

  initComponent: function() {
    this.callParent(arguments);
  }
});
