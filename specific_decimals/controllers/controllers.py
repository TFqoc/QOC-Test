# -*- coding: utf-8 -*-
# from odoo import http


# class SpecificDecimals(http.Controller):
#     @http.route('/specific_decimals/specific_decimals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/specific_decimals/specific_decimals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('specific_decimals.listing', {
#             'root': '/specific_decimals/specific_decimals',
#             'objects': http.request.env['specific_decimals.specific_decimals'].search([]),
#         })

#     @http.route('/specific_decimals/specific_decimals/objects/<model("specific_decimals.specific_decimals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('specific_decimals.object', {
#             'object': obj
#         })
