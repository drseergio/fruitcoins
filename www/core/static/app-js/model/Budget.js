Ext.define('moneypit.model.Budget', {
  extend        : 'moneypit.model.Moneypit',
  fields        : [
      'id',
      'name',
      'year' ],

  proxy         : {
    type: 'rest',
    url : '/api/budget'
  },

  update_summary: function(panel) {
    var data = {
      'name'    : this.get('name'),
      'year' : this.get('year'),
    };
    var color = this.get_color(this.get('balance'));
    var tpl = Ext.create('Ext.XTemplate',
        '<div class="summary-header">&nbsp;</div>',
        '<div class="summary-inside">',
        'Viewing budget <b>{name}</b> for <b>{year}</b>',
        '</div>');
    tpl.overwrite(panel.body, data);
  },
});
