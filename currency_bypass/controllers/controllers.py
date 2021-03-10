# -*- coding: utf-8 -*-
# from odoo import http


# class CurrencyBypass(http.Controller):
#     @http.route('/currency_bypass/currency_bypass/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/currency_bypass/currency_bypass/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('currency_bypass.listing', {
#             'root': '/currency_bypass/currency_bypass',
#             'objects': http.request.env['currency_bypass.currency_bypass'].search([]),
#         })

#     @http.route('/currency_bypass/currency_bypass/objects/<model("currency_bypass.currency_bypass"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('currency_bypass.object', {
#             'object': obj
#         })
