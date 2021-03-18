# -*- coding: utf-8 -*-

from odoo import models, fields, api


class early_invoice(models.Model):
    _inherit = 'sale.order'

    has_invoice = fields.Boolean(compute="_has_invoice_compute", store=True)

    def _has_invoice_compute(self):
        for record in self:
            record.has_invoice = len(record.invoice_ids) > 0
