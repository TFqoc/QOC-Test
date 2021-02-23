# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    version = fields.Integer()

