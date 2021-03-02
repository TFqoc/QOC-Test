# -*- coding: utf-8 -*-
# from odoo import http


# class QocSalesOrderDeliverySchedule(http.Controller):
#     @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qoc_sales_order_delivery_schedule.listing', {
#             'root': '/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule',
#             'objects': http.request.env['qoc_sales_order_delivery_schedule.qoc_sales_order_delivery_schedule'].search([]),
#         })

#     @http.route('/qoc_sales_order_delivery_schedule/qoc_sales_order_delivery_schedule/objects/<model("qoc_sales_order_delivery_schedule.qoc_sales_order_delivery_schedule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qoc_sales_order_delivery_schedule.object', {
#             'object': obj
#         })
