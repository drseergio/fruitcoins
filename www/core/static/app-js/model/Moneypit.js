Ext.define('moneypit.model.Moneypit', {
  extend        : 'Ext.data.Model',

  change_sign   : function(val) {
    var fvalue = parseFloat(val);
    return Math.abs(fvalue).toFixed(2);
  },

  get_color     : function(val) {
    var fvalue = parseFloat(val);
    if (fvalue < 0) {
      return 'red';
    } else if (fvalue > 0) {
      return 'green';
    } else {
      return 'black';
    }
  }
});
