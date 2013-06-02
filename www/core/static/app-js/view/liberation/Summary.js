Ext.define('moneypit.view.liberation.Summary', {
  extend       : 'Ext.Panel',
  alias        : 'widget.liberationsummary',
  border       : false,

  height       : 65,
  html         : '<div class="summary-header">&nbsp;</div><div class="summary-inside"><div>The purpose of liberation is to allow you to both, <b>import</b> and <b>export</b> data</div><div>Currently <b>KMyMoney</b> format is supported for full import/export<div>The process might take up to 10 minutes, it is advisable <b>not to use fruitcoins during this time</b></div></div></div>',
  cls          : 'summary',

  initComponent: function() {
    this.callParent(arguments);
  }
});
