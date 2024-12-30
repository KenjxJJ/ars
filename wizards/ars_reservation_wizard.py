# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateBookingWizard(models.TransientModel):
    _name = "ars.reservation.wizard"
    _description = "Create Booking Wizard"
    _rec_name = 'passenger_id'

    passenger_id = fields.Many2one('ars.passenger')
    flight_bk_id = fields.Many2one('ars.flight', string="Flight")
    book_datetime = fields.Datetime(default=datetime.now())
    available_seats = fields.Integer(related='flight_bk_id.available_seats')
    remaining_seats = fields.Integer(default=0)
    total_seats_requested = fields.Integer(string='Seats Booked',
                                           help='Requested number of seats or number of tickets to make!',
                                           default=1)
    create_tickets = fields.Boolean(default=False, store=False)

    @api.constrains('total_seats_requested')
    def _check_total_seats_requested(self):
        for rec in self:
            if rec.total_seats_requested < 1:
                raise UserError("Please select atleast one seat of booking before confirmation.")

    def book_now(self):
        for record in self:
            book_obj = self.env['ars.reservation']
            bk_details = {}
            ticket_details = {}

            # Update status
            if record.total_seats_requested > 0:
                record.create_tickets = True

            bk_details = {
                'passenger_id': record.passenger_id.id if record.passenger_id else False,
                'flight_bk_id': record.flight_bk_id.id if record.flight_bk_id else False,
                'book_datetime': record.book_datetime,
            }

            ticket_details = {
                'flight_ticket_id': record.flight_bk_id.id,
                'ticket_price': 100
            }
            ticket_ids = [(0, 0, ticket_details) for seat in range(record.total_seats_requested)]

            bk_details['ticket_ids'] = ticket_ids
            bk = book_obj.create(bk_details)
            bk.write({
                'name': record.flight_bk_id.display_name + "/" + str(bk.id),
            })

            return {
                "name": _("Booking ID %d") % bk.id,
                "view_type": "form",
                "res_model": "ars.reservation",
                "res_id": bk.id,
                "view_id": self.env.ref('ars.ars_reservation_view_form').id,
                "view_mode": "form",
                "type": "ir.actions.act_window",
                "target": "new",
            }

