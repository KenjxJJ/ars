from email.policy import default

from odoo import models, fields, api, _


class AircraftTicket(models.Model):
    _name = "ars.ticket"
    _description = "Ticket Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "ticket_no"

    ticket_no = fields.Char(string="Ticket No.", default='/', readonly=True, copy=False)
    book_ref = fields.Many2one("ars.reservation", string="Booking ID")
    passenger_id = fields.Many2one('ars.passenger',string="Passenger Name")
    contact_data = fields.Text(string="Contact Information", compute='_compute_contact_info')

    # Flight Information
    flight_ticket_id = fields.Many2one('ars.flight', string="Flight Number")
    flight_available_seats = fields.Integer(string='Available Seats',
                                            related='flight_ticket_id.available_seats')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency',compute='_compute_company_currency')
    ticket_price = fields.Monetary(string='Price',
                                   store=True,
                                   currency_field='currency_id',
                                   compute='_compute_flight_price_ticket')

    @api.onchange('book_ref')
    def _onchange_flight_number(self):
        for rec in self:
            if rec.book_ref:
                rec.flight_ticket_id = rec.book_ref.flight_bk_id

    @api.depends('company_id')
    def _compute_company_currency(self):
        for rec in self:
            if rec.company_id:
                rec.currency_id = rec.company_id.currency_id
            else:
                curr = self.env['res.currency'].search([], limit=1)
                rec.currency_id = curr.id

    @api.model
    def create(self, vals_list):
        ticket = super(AircraftTicket, self).create(vals_list)

        for rec, val in zip(ticket, vals_list):
            flight_ref = self.env['ars.flight'].browse(rec.flight_ticket_id.id).flight_no
            if flight_ref:
                rec['ticket_no'] = f'{flight_ref}/TK000{ticket.id}'
            else:
                rec['ticket_no'] = f'TK000{ticket.id}'
        return ticket

    @api.depends('flight_ticket_id')
    def _compute_flight_price_ticket(self):
        for rec in self:
            fl_price = rec.flight_ticket_id.cost_price if rec.flight_ticket_id else 0.0
            rec.ticket_price = fl_price

    @api.depends('passenger_id')
    def _compute_contact_info(self):
        for rec in self:
            rec.contact_data = ''

            if rec.passenger_id:
                street = rec.passenger_id.street if rec.passenger_id.street else ""
                email = rec.passenger_id.email if rec.passenger_id.email else ""
                mobile = rec.passenger_id.mobile if rec.passenger_id.mobile else ""
                city = rec.passenger_id.city if rec.passenger_id.city else ""
                rec.contact_data = f'Tel: {mobile}\nEmail: {email}\nStreet: {street}\nCity: {city}'
            else:
                rec.contact_data = ''

