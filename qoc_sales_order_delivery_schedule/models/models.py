# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qoc_sales_order_delivery_schedule(models.Model):
    _name = 'qoc.sales_order_delivery_schedule'
    _description = 'Sales Order Delivery Schedule'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def my_method(self):
        pass

class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    def get_mo_records(self):
        return self.env['mrp.production'].search([('product_id','=',self.product_id.id)],limit=80,order="id desc")

class Production(models.Model):
    _inherit = 'mrp.production'

    def get_wo_records(self):
        return self.env['mrp.workorder'].search([('production_id','=',self.id)],limit=80)
# class View(models.Model):
#     _inherit = 'ir.ui.view'

#     type = fields.Selection(selection_add=[('delivery_schedule','Delivery Schedule')])

# class ActWindowView(models.Model):
#     _inherit = 'ir.actions.act_window.view'

#     view_mode = fields.Selection(selection_add=[('delivery_schedule','Delivery Schedule')])