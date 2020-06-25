# -*- coding: utf-8 -*-
from odoo import http

# class CyclePackaging(http.Controller):
#     @http.route('/cycle_packaging/cycle_packaging/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cycle_packaging/cycle_packaging/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cycle_packaging.listing', {
#             'root': '/cycle_packaging/cycle_packaging',
#             'objects': http.request.env['cycle_packaging.cycle_packaging'].search([]),
#         })

#     @http.route('/cycle_packaging/cycle_packaging/objects/<model("cycle_packaging.cycle_packaging"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cycle_packaging.object', {
#             'object': obj
#         })