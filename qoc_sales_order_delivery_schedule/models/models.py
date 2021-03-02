# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qoc_sales_order_delivery_schedule(models.Model):
    _name = 'qoc.sales_order_delivery_schedule'
    _description = 'Sales Order Delivery Schedule'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def my_method(self):
        pass