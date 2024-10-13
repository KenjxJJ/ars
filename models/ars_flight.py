# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AircraftFlight(models.Model):
    _name = "ars.flight"
    _description = "Aircraft Flight Information"
    _rec_name = 'flight_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Scheduled Information
    flight_no = fields.Char("Flight Number")
    scheduled_departure = fields.Datetime()
    scheduled_arrival = fields.Datetime()
    departure_airport = fields.Many2one("ars.airport")
    arrival_airport = fields.Many2one("ars.airport")
    status = fields.Selection([('draft', 'Not Set'),
                               ('pending', 'Pending'),
                               ('depart', 'Departed'),
                               ('arrived', 'Completed'),
                               ('cancel', 'Cancelled')], default='draft')
    aircraft_code = fields.Char(string="Airport Code")

    # Actual Flight Information
    actual_departure = fields.Datetime()
    actual_arrival = fields.Datetime()

    # Booking Information
    booking_ids = fields.One2many('ars.reservation', 'flight_bk_id', string='Flight Bookings')
    booking_no = fields.Integer('Total Bookings', compute="_compute_bookings_no")
    tickets_no = fields.Integer('Passenger Tickets', compute="_compute_bookings_no")
    flight_ticket_ids = fields.One2many('ars.ticket', 'flight_ticket_id', string='Passenger Tickets')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', compute='_compute_company_currency',\
                                  default=lambda self: self.env.user.company_id.currency_id)
    cost_price = fields.Monetary(string='Cost Price', default=0, currency_field='currency_id', store=True)
    total_seats = fields.Integer(string='Total Seats', default=0)
    available_seats = fields.Integer(string='Total Seats', default=0)

    @api.depends('booking_ids')
    def _compute_bookings_no(self):
        for rec in self:
            if rec.booking_ids:
                rec.booking_no = len(rec.booking_ids)
                rec.tickets_no = len(rec.booking_ids.ticket_ids)
            else:
                rec.booking_no = 0
                rec.tickets_no = 0

    @api.depends('company_id')
    def _compute_company_currency(self):
        for rec in self:
            if rec.company_id:
                rec.currency_id = rec.company_id.currency_id
            else:
                curr = self.env['res.currency'].search([], limit=1)
                rec.currency_id = curr.id

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------

    def action_create_booking(self):
        for rec in self:
            return {
                "name": "Create Booking",
                "view_type": "form",
                "res_model": "ars.reservation.wizard",
                "view_id": self.env.ref('ars.ars_reservation_wizard_form_view').id,
                "view_mode": "form",
                "type": "ir.actions.act_window",
                "target": "new",
                "context": {'create': False},
            }

    def action_view_bookings(self):
        for rec in self:
            return {
                "name": _("Flight Bookings - %s") % rec.flight_no,
                "domain": [('flight_bk_id', '=', rec.id)],
                "res_model": "ars.reservation",
                "view_mode": "tree,form",
                "type": "ir.actions.act_window",
                "context": {'create': False},
            }

    def action_view_tickets(self):
        for rec in self:
            return {
                "name": _("Flight Bookings - %s") % rec.flight_no,
                "domain": [('flight_ticket_id', 'in', rec.ids)],
                "res_model": "ars.ticket",
                "view_mode": "tree,form",
                "type": "ir.actions.act_window",
                "context": {'create': False},
            }
