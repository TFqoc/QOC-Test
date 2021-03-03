odoo.define('qoc.monetary_decimals', function (require) {
    "use strict";

    var monetary = require('web.basic_fields').FieldMonetary;
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
            this.formatOptions.digits = [16, 6];
            this.formatOptions.field_digits = this.nodeOptions.field_digits;
        },
    });
    fieldRegistry.add('monetary_decimals', MonetaryDecimals);
});