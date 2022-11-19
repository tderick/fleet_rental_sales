from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

logger = logging.getLogger(__name__)

# DESCRIPTION_SALE = """
# Numéro DE SERIE: <b>{}</b>
# IMMAT: <b>{}</b>
# Mise en circulation: <b>{}</b>
# Carburant: <b>{}</b>
# KM: <b>{} {}</b>
# """

DESCRIPTION_SALE = """
Numéro DE SERIE: {}
IMMAT: {}
Mise en circulation: {}
Carburant: {}
KM: {} {}
"""


class FleetVehicleExtend(models.Model):
    _inherit = "fleet.vehicle"

    license_plate = fields.Char(
        required=True, help="Plate d'immatriculation sans espace ni caractères spéciaux")

    sale_ok = fields.Boolean(string="Peut être vendu", default=False)
    rent_ok = fields.Boolean(string="Peut être loué", default=False)

    @api.constrains('license_plate')
    def _constrain_licence_plate_valid(self):
        for record in self:
            if not self.license_plate.isalnum():
                raise ValidationError(
                    "Plaque d'immatricuation invalide. Utilisez uniquement des lettres et des chiffres sans espace.")

    def write(self, values):
        Fleet = self.env['fleet.vehicle']

        # Old vehicle name before update
        # This name is used to find the corresponding product after update
        old_fleet_name = Fleet.browse(self.id).name

        overwrite_write = super(FleetVehicleExtend, self).write(values)

        # Get the updated vehicle
        fleet = Fleet.browse(self.id)

        Product = self.env['product.template']

        description = DESCRIPTION_SALE.format("",
                                              fleet.license_plate, fleet.acquisition_date, fleet.fuel_type, fleet.odometer, fleet.odometer_unit)

        # If the product can be sold
        if fleet.sale_ok:

            if Product.search_count([('name', 'like', old_fleet_name)]) >= 1:
                product = Product.search(
                    [('name', 'like', old_fleet_name)])
                product.update({
                    "name": fleet.name,
                    "standard_price": fleet.net_car_value,
                    "active": True,
                    "description_sale": description
                })
            else:
                Product.create({
                    "name": fleet.name,
                    "standard_price": fleet.net_car_value,
                    "type": "product",
                    "description_sale": description
                })
        else:
            if Product.search_count([('name', 'like', old_fleet_name)]) >= 1:
                product = Product.search(
                    [('name', '=', old_fleet_name)], limit=1)
                product.update({"active": False})

        return overwrite_write
