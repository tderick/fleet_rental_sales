import logging

from odoo import fields, models, api


logger = logging.getLogger(__name__)


class FleetVehicleModelExtend(models.Model):
    _inherit = "fleet.vehicle.model"

    vehicle_type = fields.Selection(selection_add=[(
        'camion', 'Camion'), ('camionnette', 'Camionnette'), ('monte-meuble', 'Monte-meuble')],
        ondelete={'camion': 'set default', 'camionnette': 'set default', 'monte-meuble': 'set default'})
