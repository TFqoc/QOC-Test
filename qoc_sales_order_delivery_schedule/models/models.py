# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qoc_sales_order_delivery_schedule(models.Model):
    _name = 'qoc.sales_order_delivery_schedule'
    _description = 'Sales Order Delivery Schedule'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def my_method(self):
        pass