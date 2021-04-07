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
            order = self.env['purchase.order'].browse(action['context']['active_id'])
            ids = []
            for line in order.order_line:
                if line.product_id.part_print:
                    ids.append(self.env['ir.attachment'].create({
                        'name':'Part Print.pdf',
                        'type':'binary',
                        'res_model':'mail.compose.message',
                        # 'db_datas':line.product_id.part_print,
                        'datas':line.product_id.part_print,
                    }).id)
                    _logger.info("FOUND AN ATTACHMENT")
            _logger.info("UPDATING CONTEXT")
            action['context'].update({
                'default_attachment_ids': ids,# [(6,0,ids)],
                'default_dummy_field': str(ids),
            })
        _logger.info("RETURNING ACTION WITH CONTEXT: " + str(action['context']))
        return action

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    dummy_field = fields.Char()

    # @api.model
    # def default_get(self, fields):
    #     _logger.info("GETTING DEFAULTS")
    #     res = super(MailComposer, self).default_get(fields)
    #     if 'default_attachment_ids' in self._context:
    #         _logger.info("ADDING ATTACHMENTS: " + str(self._context['default_attachment_ids']))
    #         attachment_ids = self._context['default_attachment_ids']
    #         res.update({
    #             'attachment_ids':attachment_ids,
    #         })
    #     return res

    # @api.model
    # def create(self, vals):
    #     res = super(MailComposer, self).create(vals)
    #     # This method is never called
    #     _logger.info("CREATE METHOD CALLED")
    #     return res

    @api.onchange('attachment_ids')
    def change_attachment_ids(self):
        _logger.info("ATTACHMENTS WERE: " + str(self._origin.attachment_ids))
        _logger.info("ATTACHMENTS ARE: " + str(self.attachment_ids))