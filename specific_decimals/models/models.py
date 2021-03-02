# -*- coding: utf-8 -*-

from odoo import models, fields, api

class specific_decimals(models.Model):
    _inherit = 'purchase.order.line'

    price_unit = fields.Float(string='Unit Price', required=True, digits='Purchase Price')