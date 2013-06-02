Ext.define('moneypit.model.Category', {
  extend: 'moneypit.model.Moneypit',
  fields: [
      'id',
      'text',
      'description',
      'parent',
      'total_balance',
      'balance'],

  proxy       : {
    type: 'rest',
    url : '/api/category'
  },

  update_summary: function(panel) {
    var data = {
      'name'         : this.get('text'),
      'currency'     : wealthCurrency
    };
    data.total_balance = this.change_sign(this.get('total_balance'));
    data.balance = this.change_sign(this.get('balance'));
    var total_color = this.get_color(this.get('total_balance'));
    var balance_color = this.get_color(this.get('balance'));

    var tpl = Ext.create('Ext.XTemplate',
        '<div class="summary-header">&nbsp;</div>',
        '<div class="summary-inside">',
        'Viewing transactions for category <b>{name}</b>',
        '<div class="summary-amount">',
        '<div class="summary-amount-header">balance</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 2em;color:',total_color,'">',
        '{total_balance:currency}</span> ',
        '<span style="font-size: 2em;color:',balance_color,'">',
        '({balance:currency})</span> {currency}</div></div>',
        '</div>');
    tpl.overwrite(panel.body, data);
  },
});
