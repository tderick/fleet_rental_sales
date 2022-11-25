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
    odometer = fields.Float(required=True)
    acquisition_date = fields.Date(required=True)
    vin_sn = fields.Char(required=True)
    net_car_value = fields.Float(required=True)
    seats = fields.Integer(required=True)
    transmission = fields.Selection(required=True)
    fuel_type = fields.Selection(required=True)

    rent_ok = fields.Boolean(string="Peut être loué", default=False)

    taxes_id = fields.Many2many(
        "account.tax", string="Taxes à la vente", required=True)

    @api.constrains('license_plate')
    def _constrain_licence_plate_valid(self):
        for record in self:
            if not self.license_plate.isalnum():
                raise ValidationError(
                    "Plaque d'immatricuation invalide. Utilisez uniquement des lettres et des chiffres sans espace.")

    @api.constrains('seats')
    def _constrain_seats_non_nul(self):
        for record in self:
            if record.seats <= 0:
                raise ValidationError(
                    "Le nombre de places dans le véhicule ne peut être nul ou négatif. Veuillez entrer une valeur supérieure à 0")

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

        if Product.search_count([('name', 'like', old_fleet_name)]) >= 1:
            product = Product.search(
                [('name', 'like', old_fleet_name)])
            product.update({
                "name": fleet.name,
                "taxes_id": fleet.taxes_id,
                "description_sale": description
            })
        else:
            product = Product.create({
                "name": fleet.name,
                "type": "product",
                "taxes_id": fleet.taxes_id,
                "description_sale": description,
                "is_vehicle": True
            })

            # Create the initial stock for the product and set it to 1
            warehouse = self.env['stock.warehouse'].search([], limit=1)
            self.env['stock.quant'].sudo().create({
                'product_id': product.id,
                'inventory_quantity': 1,
                'available_quantity': 1,
                'quantity': 1,
                'location_id': warehouse.lot_stock_id.id,
            })

        return overwrite_write

    def unlink(self):
        fleet_name = self.name
        override_unlink = super(FleetVehicleExtend, self).unlink()
        self.env['product.template'].search(
            [('name', '=', fleet_name)]).unlink()
        return override_unlink
