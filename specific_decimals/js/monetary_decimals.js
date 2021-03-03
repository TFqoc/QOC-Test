odoo.define('qoc.monetary_decimals', function (require) {
    "use strict";

    var monetary = require('web.basic_fields').FieldMonetary;
    var field_utils = require('web.field_utils');
    var fieldRegistry = require('web.field_registry');

    var MonetaryDecimals = monetary.extend({
        init: function () {
            this._super.apply(this, arguments);
    
            this._setCurrency();
    
            if (this.mode === 'edit') {
                this.tagName = 'div';
                this.className += ' o_input';
    
                // do not display currency symbol in edit
                this.formatOptions.noSymbol = true;
            }
    
            this.formatOptions.currency = this.currency;
            console.log(typeof(this.formatOptions.currency.digits));
            console.log(typeof(this.formatOptions.currency));
            this.formatOptions.currency.digits[1] = 2;
            this.formatOptions.digits = [16, 2];
            this.formatOptions.field_digits = 2;
        },
        _renderReadonly: function () {
            this.$el.html(this._formatValue(this.value));
        },
    });
    fieldRegistry.add('monetary_decimals', MonetaryDecimals);
});