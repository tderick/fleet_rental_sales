import logging

from odoo import fields, models, api


logger = logging.getLogger(__name__)


class ProductExtend(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(
        readonly=True, compute="_compute_standard_price")

    product_price = fields.Float(string="Prix du produit")

    is_vehicle = fields.Boolean(default=False)

    def _compute_standard_price(self):
        """"Compute the standard_price dynamically based on the invoice associate to it.
        When an invoice is produced for an action on a vehicle, the *cost price(a.k.a standard_price)* 
        of the vehicle is increased with the total amount of the vehicle.

        1. Loop through each record
        2. Search the vehicle associated to the current product
        3. Use the found vehicle to get all the validated invoice associated to that vehicle
        4. Loop through each invoice and add the total amount to the standard_price of the product
        """

        for product in self:
            # Search the vehicle associated to the current product
            vehicle = self.env['fleet.vehicle'].search(
                [("name", "=", product.name)], limit=1)

            if len(vehicle) == 1:

                # The first price of the product is the net car value price from fleet
                product.standard_price = vehicle.net_car_value

                # Use the found vehicle to get all the validated invoice associated to that vehicle
                invoices = self.env['account.move'].search(
                    ['&', ('vehicle_id', "=", vehicle.id), ("state", "=", "posted")])

                # Loop through each invoice and add the total amount to the standard_price of the product
                for invoice in invoices:
                    product.standard_price += invoice.amount_total
            else:
                product.standard_price = product.product_price

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain += [("active", "=", True)]
        res = super(ProductExtend, self).search_read(
            domain, fields, offset, limit, order)

        return res

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        args = args or []
        domain = [("active", "=", True)]
        return self._search(domain+args, limit=limit, access_rights_uid=name_get_uid)
