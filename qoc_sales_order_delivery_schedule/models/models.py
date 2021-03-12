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
    def get_delivery_records(self):
        return self.env['stock.picking'].search([('sale_id','=',self.order_id.id)],limit=80,order="id desc")

class Production(models.Model):
    _inherit = 'mrp.production'

    def get_wo_records(self):
        return self.env['mrp.workorder'].search([('production_id','=',self.id)],limit=80)

class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    def get_consumed_components(self):
        res = {}
        for op in self.production_bom_id.operation_ids:
            res[op.name] = []
        for line in self.production_id.raw_move_ids:
            if line.operation_id:
                res[line.operation_id.name].append()
        return res