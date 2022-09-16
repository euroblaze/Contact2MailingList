odoo.define('settings.drip', function (require) {
"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
                let filter_button = this.$buttons.find('.oe_new_button');
                filter_button && filter_button.click(this.proxy('mail_drip')) ;
            }
        },
        filter_button: function () {
            console.log('yay filter')
        }
    });
})