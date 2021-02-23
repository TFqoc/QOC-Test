# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    version = fields.Integer()

    # @api.model
    # def _prepare_add_missing_fields(self, values):
    #     """ Deduce missing required fields from the onchange """
    #     res = {}
    #     onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id', 'version']
    #     if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
    #         line = self.new(values)
    #         line.product_id_change()
    #         for field in onchange_fields:
    #             if field not in values:
    #                 res[field] = line._fields[field].convert_to_write(line[field], line)
    #     return res

