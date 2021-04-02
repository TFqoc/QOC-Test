# -*- coding: utf-8 -*-
# from odoo import http


# class PartPrints(http.Controller):
#     @http.route('/part_prints/part_prints/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/part_prints/part_prints/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('part_prints.listing', {
#             'root': '/part_prints/part_prints',
#             'objects': http.request.env['part_prints.part_prints'].search([]),
#         })

#     @http.route('/part_prints/part_prints/objects/<model("part_prints.part_prints"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('part_prints.object', {
#             'object': obj
#         })
