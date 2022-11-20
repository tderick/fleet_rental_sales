import logging

from odoo import fields, models, api


logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    vehicle_id = fields.Many2one(
        "fleet.vehicle", string="Véhicule concerné")
