from odoo import models, api, fields, _

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    booking_ids = fields.One2many('ars.reservation', 'invoice_id', string="Invoiced Bookings")