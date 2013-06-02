Ext.define('moneypit.controller.Currency', {
  extend: 'Ext.app.Controller',
  views : [ 'fx.Combobox' ],
  stores: [ 'Currency' ],
  models: [ 'Currency' ],

  init: function() {
  },
});
