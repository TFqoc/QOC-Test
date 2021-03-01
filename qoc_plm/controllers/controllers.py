# -*- coding: utf-8 -*-
# from odoo import http


# class Plm2(http.Controller):
#     @http.route('/plm2/plm2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plm2/plm2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plm2.listing', {
#             'root': '/plm2/plm2',
#             'objects': http.request.env['plm2.plm2'].search([]),
#         })

#     @http.route('/plm2/plm2/objects/<model("plm2.plm2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plm2.object', {
#             'object': obj
#         })
