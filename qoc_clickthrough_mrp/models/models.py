# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qoc_clickthrough_mrp(models.Model):
    _inherit = 'mrp.production'

    #source_documents = fields.Many2many(comodel_name='')

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100