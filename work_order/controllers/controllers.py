# -*- coding: utf-8 -*-
# from odoo import http


# class WorkOrder(http.Controller):
#     @http.route('/work_order/work_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/work_order/work_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('work_order.listing', {
#             'root': '/work_order/work_order',
#             'objects': http.request.env['work_order.work_order'].search([]),
#         })

#     @http.route('/work_order/work_order/objects/<model("work_order.work_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('work_order.object', {
#             'object': obj
#         })
