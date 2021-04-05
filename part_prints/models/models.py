# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    part_print = fields.Binary(string="Print for Vendor PO")

class Product(models.Model):
    _inherit = 'product.product'
    
    part_print = fields.Binary(related='product_tmpl_id.part_print')

class BOM(models.Model):
    _inherit = 'mrp.bom'

    part_print = fields.Binary(string="Print File")

class MRP(models.Model):
    _inherit = 'mrp.production'
    
    part_print = fields.Binary(related='bom_id.part_print')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_rfq_send(self):
        # Do some cool stuff to add all the attachments to the email
        # purchase.py line 305
        # Check the template used and see if you can edit that to put attachements there.
        action = super(PurchaseOrder, self).action_rfq_send()
        if action['context']['active_model'] == 'purchase.order':
            _logger.info("GATHERING ATTACHMENTS")
            order = self.env['purchase.order'].browse(self.env.context['active_id'])
            ids = []
            for line in order.order_line:
                if line.product_id.part_print:
                    ids.append(self.env['ir.attachment'].create({
                        'name':'Part Print',
                        'type':'binary',
                        'db_datas':line.product_id.part_print,
                    }).id)
            action.update({
                'default_attachment_ids': [(6,0,ids)],
            })

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def create(self, vals):
        _logger.info("CREATING WIZARD")
        if self.env.context['active_model'] == 'purchase.order':
            _logger.info("GATHERING ATTACHMENTS")
            order = self.env.browse(self.env.context['active_id'])
            ids = []
            for line in order.order_line:
                if line.product_id.part_print:
                    ids.append(self.env['ir.attachment'].create({
                        'name':'Part Print',
                        'type':'binary',
                        'db_datas':line.product_id.part_print,
                    }).id)
            vals.update({
                'attachment_ids': [(6,0,ids)],
            })
        return super(MailComposer, self).create(vals)