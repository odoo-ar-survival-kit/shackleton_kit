# -*- coding: utf-8 -*-
# from odoo import http


# class PosNoweb(http.Controller):
#     @http.route('/pos_noweb/pos_noweb/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_noweb/pos_noweb/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_noweb.listing', {
#             'root': '/pos_noweb/pos_noweb',
#             'objects': http.request.env['pos_noweb.pos_noweb'].search([]),
#         })

#     @http.route('/pos_noweb/pos_noweb/objects/<model("pos_noweb.pos_noweb"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_noweb.object', {
#             'object': obj
#         })
