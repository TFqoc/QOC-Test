from odoo import models, fields, api

class MRP(models.Model):
    _inherit = 'mrp.production'

    rma_id = fields.Many2one('rma.rma', readonly=True)

    #TODO don't produce the product if we have an RMA attached