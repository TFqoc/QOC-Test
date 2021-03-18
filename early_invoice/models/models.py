# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class early_invoice(models.Model):
    _inherit = 'sale.order'

    has_invoice = fields.Boolean(compute="_has_invoice_compute", store=True)

    @api.depends('invoice_ids')
    def _has_invoice_compute(self):
        for record in self:
            record.has_invoice = len(record.invoice_ids.ids) > 0
            _logger.info("\nLEN: "+str(len(record.invoice_ids.ids)))
