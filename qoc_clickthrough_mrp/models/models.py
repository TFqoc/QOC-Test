# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class qoc_clickthrough_mrp(models.Model):
#     _name = 'qoc_clickthrough_mrp.qoc_clickthrough_mrp'
#     _description = 'qoc_clickthrough_mrp.qoc_clickthrough_mrp'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
