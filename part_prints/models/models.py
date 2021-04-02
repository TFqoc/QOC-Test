# -*- coding: utf-8 -*-

from odoo import models, fields, api


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