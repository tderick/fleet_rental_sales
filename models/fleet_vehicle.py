from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

logger = logging.getLogger(__name__)


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

        # Get the translated value of fuel_type
        fuel_type = dict(self._fields['fuel_type']._description_selection(
            self.env)).get(fleet.fuel_type)
        # Get the translated value of odometer_unit
        odometer_unit = dict(self._fields['odometer_unit']._description_selection(
            self.env)).get(fleet.odometer_unit)

        description = DESCRIPTION_SALE.format(fleet.vin_sn,
                                              fleet.license_plate, fleet.acquisition_date, fuel_type, fleet.odometer, odometer_unit)

        # If the product can be sold
        if fleet.sale_ok:

            if Product.search_count([('name', 'like', old_fleet_name)]) >= 1:
                product = Product.search(
                    [('name', 'like', old_fleet_name)])
                product.update({
                    "name": fleet.name,
                    "active": True,
                    "description_sale": description
                })
            else:
                product = Product.create({
                    "name": fleet.name,
                    "type": "product",
                    "description_sale": description,
                    "is_vehicle": True
                })

                # Create the initial stock for the product and set it to 1
                warehouse = self.env['stock.warehouse'].search([], limit=1)
                self.env['stock.quant'].create({
                    'product_id': product.id,
                    'inventory_quantity': 1,
                    'available_quantity': 1,
                    'quantity': 1,
                    'location_id': warehouse.lot_stock_id.id,
                })
        else:
            if Product.search_count([('name', 'like', old_fleet_name)]) >= 1:
                product = Product.search(
                    [('name', '=', old_fleet_name)], limit=1)
                product.update({"active": False})

        return overwrite_write

    def unlink(self):
        fleet_name = self.name
        override_unlink = super(FleetVehicleExtend, self).unlink()
        self.env['product.template'].search(
            [('name', '=', fleet_name)]).unlink()
        return override_unlink
