# -*- coding: utf-8 -*-

from odoo import models, fields, api

class specific_decimals(models.Model):
    _inherit = 'purchase.order.line'

    price_unit = fields.Float(string='Unit Price', required=True, digits='Purchase Price')

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True, digits='Purchase Price')
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True, digits='Purchase Price')
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True, digits='Purchase Price')