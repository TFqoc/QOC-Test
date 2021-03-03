odoo.define('qoc.monetary_decimals', function (require) {
    "use strict";

    var monetary = require('web.basic_fields').FieldMonetary;
    var field_utils = require('web.field_utils');
    var fieldRegistry = require('web.field_registry');

    var my_utils = field_utils.include({
        format2Monetary : function (value, field, options){
        //function formatMonetary(value, field, options) {
            if (value === false) {
                return "";
            }
            options = Object.assign({ forceString: false }, options);
        
            var currency = options.currency;
            if (!currency) {
                var currency_id = options.currency_id;
                if (!currency_id && options.data) {
                    var currency_field = options.currency_field || field.currency_field || 'currency_id';
                    currency_id = options.data[currency_field] && options.data[currency_field].res_id;
                }
                currency = session.get_currency(currency_id);
            }
        
            var digits = 2
            var formatted_value = formatFloat(value, field,
                _.extend({}, options , {digits: digits})
            );
        
            if (!currency || options.noSymbol) {
                return formatted_value;
            }
            const ws = options.forceString ? ' ' : '&nbsp;';
            if (currency.position === "after") {
                return formatted_value + ws + currency.symbol;
            } else {
                return currency.symbol + ws + formatted_value;
            }
        }
    });

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
            this.formatOptions.digits = [16, 2];
            this.formatOptions.field_digits = 2;
        },
    });
    fieldRegistry.add('monetary_decimals', MonetaryDecimals);
});