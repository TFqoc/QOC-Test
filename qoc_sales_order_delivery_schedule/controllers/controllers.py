# -*- coding: utf-8 -*-
from odoo import http


class DeliveryScheduleManager(http.Controller):
    @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('qoc_sales_order_delivery_schedule.listing', {
            'root': '/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule',
            'objects': http.request.env['sale.order'].search([]),
        })

    @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/objects/<model("sale.order"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('qoc_sales_order_delivery_schedule.object', {
            'object': obj
        })
    
    @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/mo_data/<model("sale.order.line"):obj>/', auth='public')
    def mo_data(self, obj, **kw):
        # data = obj.get_mo_records()
        return http.request.render('qoc_sales_order_delivery_schedule.mo_lines', {
            'objects': http.request.env['mrp.production'].search([('product_id','=',obj.product_id.id)]),
        })

    @http.route('/ds/mo_data/', auth='public')
    def mo_data(self, **kw):
        return http.request.env['mrp.production'].search([])
