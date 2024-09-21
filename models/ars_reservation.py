# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AirportReservation(models.Model):
    _name = 'ars.reservation'
    _description = 'Airport Reservation (Booking)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    name = fields.Char(string="Booking Ref", help="Reservation Number")
    book_date = fields.Date(string="Date of Booking")
    book_datetime = fields.Datetime(string="Booking Date")
    total_amount = fields.Float(string="Total Amount")

    # Tickets
    ticket_ids = fields.One2many(comodel_name="ars.ticket",
                                 inverse_name="book_ref",
                                 string="Tickets", help="Tickets as per the booking")

    # Flights
    flight_bk_id = fields.Many2one('ars.flight', string='Selected Flight')
    passenger_id = fields.Many2one('ars.passenger', string='Booked by')

    status = fields.Selection([('draft', 'Draft'), ('save', 'Set')], default='draft', string="Booking Status")

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------

    def set_booking(self):
        for rec in self:
            rec.write({'status': 'save'})

    def set_draft(self):
        for rec in self:
            rec.write({'status': 'draft'})
