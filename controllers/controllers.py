# -*- coding: utf-8 -*-
# from odoo import http


# class FleetRentalSales(http.Controller):
#     @http.route('/fleet_rental_sales/fleet_rental_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_rental_sales/fleet_rental_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_rental_sales.listing', {
#             'root': '/fleet_rental_sales/fleet_rental_sales',
#             'objects': http.request.env['fleet_rental_sales.fleet_rental_sales'].search([]),
#         })

#     @http.route('/fleet_rental_sales/fleet_rental_sales/objects/<model("fleet_rental_sales.fleet_rental_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_rental_sales.object', {
#             'object': obj
#         })
