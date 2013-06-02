MoneypitMobile.views.TransactionList = Ext.extend(Ext.List, {
  store: 'Transaction',
  itemTpl: '{description}',
  plugins: [{
      ptype: 'listpaging',
      autoPaging: false
    }, {
      ptype: 'pullrefresh'
  }],

  itemTpl         : new Ext.XTemplate(
    '<div class="account-name"><b>{date:date("d-m-Y")}</b> {category}</div>',
    '<div class="account-info">{description}</div>',
    '<div class="account-balance">',
    '{amount_real:this.renderItem} {currency}</div></div>', {
      compiled: true,
      renderItem: function(val) {
        if (val > 0) {
          return '<span style="color:green;">' + Math.abs(val).toFixed(2) + '</span>';
        } else if (val < 0) {
          return '<span style="color:red;">' + Math.abs(val).toFixed(2) + '</span>';
        }
        return val;
      }
    })
});
Ext.reg('transactions', MoneypitMobile.views.TransactionList);
