# -*- coding: utf-8 -*-
# from odoo import http


# class DriversModule(http.Controller):
#     @http.route('/drivers_module/drivers_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/drivers_module/drivers_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('drivers_module.listing', {
#             'root': '/drivers_module/drivers_module',
#             'objects': http.request.env['drivers_module.drivers_module'].search([]),
#         })

#     @http.route('/drivers_module/drivers_module/objects/<model("drivers_module.drivers_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('drivers_module.object', {
#             'object': obj
#         })
