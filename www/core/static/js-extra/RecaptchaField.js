Ext.define('Ext.ux.RecaptchaField', {
  alias: 'widget.recaptchafield',
  extend: 'Ext.form.field.Base',

  fieldSubTpl: [
    '<div id="{id}" style="height: 129px;"',
    '<tpl if="tabIdx">tabIndex="{tabIdx}" </tpl>',
    'class="{fieldCls}"></div>', {
      compiled: true,
      disableFormats: true
    }
  ], 
  constructor: function(config) {
    this.callParent([config]);
    this.theme = this.theme || 'blackglass';
    this.on('render', function() {
      this.up('form').getForm().on('actionfailed', function(form, action) {
        if (action.type == 'submit') {
          this.renderReCaptcha();
        }
      }, this);
      this.renderReCaptcha();
    });
  },
    
  renderReCaptcha: function() {
    Recaptcha.create(this.code, this.inputEl.id, {
      theme: 'blue',
      callback: Recaptcha.focus_response_field
    });
  },
    
  getRawValue: function() {
    var me = this,
    v = (me.inputEl ? me.inputEl.down('input[name=recaptcha_response_field]').getValue() : Ext.value(me.rawValue, ''));
    me.rawValue = v;
    return v;
  }
});

Ext.define('Ext.ux.RecaptchaChallenge', {
  alias: 'widget.recaptchachallengefield',
  extend: 'Ext.form.field.Hidden',

  getRawValue: function() {
    var me = this,
    v = this.up('form').getForm().findField('recaptcha_response_field').inputEl.down('input[name=recaptcha_challenge_field]').getValue();
    me.rawValue = v;
    return v;
  }
});
