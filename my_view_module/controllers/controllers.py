# -*- coding: utf-8 -*-
from odoo import http

# class MyViewModule(http.Controller):
#     @http.route('/my_view_module/my_view_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_view_module/my_view_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_view_module.listing', {
#             'root': '/my_view_module/my_view_module',
#             'objects': http.request.env['my_view_module.my_view_module'].search([]),
#         })

#     @http.route('/my_view_module/my_view_module/objects/<model("my_view_module.my_view_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_view_module.object', {
#             'object': obj
#         })