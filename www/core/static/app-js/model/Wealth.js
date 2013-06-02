Ext.define('moneypit.model.Wealth', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      'currency',
      'balance',
      'income',
      'expense' ],

  proxy         : {
    type: 'rest',
    url : '/api/wealth'
  },

  update_summary: function(panel) {
    var data = {
      'name'    : 'all accounts',
      'balance' : this.change_sign(this.get('balance')),
      'income': this.change_sign(this.get('income')),
      'expense': this.change_sign(this.get('expense')),
      'currency': this.get('currency')
    };
    var color = this.get_color(this.get('balance'));
    var tpl = Ext.create('Ext.XTemplate',
        '<div class="summary-header">&nbsp;</div>',
        '<div class="summary-inside">',
        'Viewing transactions for <b>{name}</b>',
        '<div class="summary-amount">',
        '<div class="summary-amount-header">net worth</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 2em;color:',color,'">',
        '{balance:currency}</span> {currency}</div></div>',
        '<div><div style="text-align:left" class="summary-amount-header">income &amp; expense</div>',
        '<div><span style="color:green">{income}</span> / ',
        '<span style="color:red">{expense}</span></div></div>',
        '</div>');
    tpl.overwrite(panel.body, data);
  },
});
