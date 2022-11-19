import logging

from odoo import fields, models, api


logger = logging.getLogger(__name__)


class ProductExtend(models.Model):
    _inherit = "product.template"

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain += [("active", "=", True)]
        res = super(ProductExtend, self).search_read(
            domain, fields, offset, limit, order)

        return res

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        args = args or []
        domain += [("active", "=", True)]
        return self._search(domain+args, limit=limit, access_rights_uid=name_get_uid)
