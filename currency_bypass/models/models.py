# -*- coding: utf-8 -*-

from odoo import models, fields, api


class currency_bypass(models.Model):
    _inherit = 'res.currency'

    def write(self, vals):
        super(models.Model, self).write(vals)
