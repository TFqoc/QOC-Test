# -*- coding: utf-8 -*-
# from odoo import http


# class QocClickthroughMrp(http.Controller):
#     @http.route('/qoc_clickthrough_mrp/qoc_clickthrough_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qoc_clickthrough_mrp/qoc_clickthrough_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qoc_clickthrough_mrp.listing', {
#             'root': '/qoc_clickthrough_mrp/qoc_clickthrough_mrp',
#             'objects': http.request.env['qoc_clickthrough_mrp.qoc_clickthrough_mrp'].search([]),
#         })

#     @http.route('/qoc_clickthrough_mrp/qoc_clickthrough_mrp/objects/<model("qoc_clickthrough_mrp.qoc_clickthrough_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qoc_clickthrough_mrp.object', {
#             'object': obj
#         })
