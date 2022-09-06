odoo.define('settings.drip', function (require) {
  "use strict";

  var ListController = require('web.ListController');

  ListController.include({

    renderButtons: function ($node) {
      this._super.apply(this, arguments);
      if (this.$buttons) {
        var filter_button = this.$buttons.find('.oe_new_button');
        filter_button && filter_button.click(this.proxy('mail_drip'));
      }
    },

  });

})