Ext.define('moneypit.view.report.Report', {
  extend       : 'Ext.panel.Panel',
  alias        : 'widget.reports',
  border       : false,
  html         : '<div class="emptyText">To generate a report choose <b>reporting period</b>, report <b>type</b> and press <b>Run</b></div>',

  initComponent: function() {
    this.layout = 'fit';
    this.tbar = [{
        xtype       : 'datefield',
        id          : 'report-from',
        emptyText   : 'From..',
        format      : 'Y-m-d',
        hideLabel   : true,
        width       : 100
      }, {
        xtype       : 'datefield',
        id          : 'report-to',
        emptyText   : 'To..',
        format      : 'Y-m-d',
        hideLabel   : true,
        width       : 100
      }, '->', {
        xtype       : 'combo',
        hideLabel   : true,
        emptyText   : 'Report type',
        queryMode   : 'local',
        displayField: 'text',
        valueField  : 'value',
        editable    : false,
        cls         : 'report-dropdown',
        store       : 'ReportType'
      }, {
        text        : 'Run',
        action      : 'show',
        disabled    : true,
        iconCls     : 'icons-run'
      }, {
        text        : 'Close',
        action      : 'close',
        disabled    : true,
        iconCls     : 'icons-close'
    }];
    this.callParent(arguments);
  }
});
