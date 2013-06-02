Ext.define('moneypit.model.Account', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      'id',
      'name',
      'balance',
      'currency',
      {name: 'type', type: 'int'} ],

  proxy         : {
    type: 'rest',
    url : '/api/account'
  },
  update_summary: function(panel) {
    var data = {
      'name'    : this.get('name'),
      'balance' : this.get('balance'),
      'currency': this.get('currency')
    };
    var color = this.get_color(this.get('balance'));
    var tpl = Ext.create('Ext.XTemplate',
        '<div class="summary-header">&nbsp;</div>',
        '<div class="summary-inside">',
        'Viewing transactions for account <b>{name}</b>',
        '<div class="summary-amount">',
        '<div class="summary-amount-header">balance</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 2em;color:',color,'">',
        '{balance:currency}</span> {currency}</div></div>',
        '</div>');
    tpl.overwrite(panel.body, data);
  }
});
