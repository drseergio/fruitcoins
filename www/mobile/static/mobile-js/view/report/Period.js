MoneypitMobile.views.Period = Ext.extend(Ext.form.FormPanel, {
  scroll        : 'vertical',
  standardSubmit: false,

  items         : [{
    xtype       : 'fieldset',
    title       : 'Generate report',
    instructions: 'Choose report type and what time-frame you are interested in',
    defaults    : {
      required  : true,
      labelAlign: 'left',
      labelWidth: '45%'
    },
    items       : [{
        xtype: 'selectfield',
        name: 'report_type',
        label: 'Report',
        options: [{
            text: 'Net worth monthly',
            value: 'NetWorth'
          }, {
            text: 'Net income monthly',
            value: 'NetIncome'
          }, {
            text: 'Expenses monthly',
            value: 'Expenses'
          }, {
            text: 'Incomes monthly',
            value: 'Incomes'
          }, {
            text: 'Expense breakdown',
            value: 'ExpenseBreakdown'
          }, {
            text: 'Income breakdown',
            value: 'IncomeBreakdown'
        }]
      }, {
        xtype       : 'datepickerfield',
        name        : 'date_from',
        label       : 'From',
        value       : new Date(),
        useClearIcon: true
      }, {
        xtype       : 'datepickerfield',
        name        : 'date_to',
        label       : 'To',
        value       : new Date(),
        useClearIcon: false
      }]
    }],
    dockedItems   : [{
      xtype: 'toolbar',
      dock: 'top',
      items: [{
          xtype: 'spacer'
        }, {
          id: 'run-report',
          text: 'Run!',
          ui: 'confirm',
      }]
    }]
});
Ext.reg('period', MoneypitMobile.views.Period);
