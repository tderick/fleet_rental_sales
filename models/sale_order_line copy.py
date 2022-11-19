from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_id = fields.Many2one("fleet.vehicle", string="Véhicule")
    product_template_id = fields.Many2one(
        "fleet.vehicle.model", string="Modèle de vehicule")
    product_uom = fields.Many2one("uom.uom", string="Unité")
