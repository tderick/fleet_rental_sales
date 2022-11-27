import logging

from odoo import fields, models, api


logger = logging.getLogger(__name__)


class SimpleProductExtend(models.Model):
    _inherit = "product.product"

    cost = fields.Float(
        readonly=True, compute="_compute_cost")

    def _compute_cost(self):

        for product in self:
            product.cost = 0.0
            product_template = self.env['product.template'].search(
                [('name', '=', self.name)], limit=1)

            if len(product_template) >= 1:
                product.cost = product_template.standard_price
            else:
                product.cost = 0.0

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        args = args or []
        domain = [("active", "=", True), ('qty_available', '>', 0)]
        return self._search(domain+args, limit=limit, access_rights_uid=name_get_uid)
