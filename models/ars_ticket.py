from odoo import models, fields, api, _


class AircraftTicket(models.Model):
    _name = "ars.ticket"
    _description = "Ticket Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "ticket_no"

    ticket_no = fields.Char(string="Ticket No.", default='/', readonly=True, copy=False)
    book_ref = fields.Many2one("ars.reservation", string="Booking ID")
    passenger_id = fields.Many2one('ars.passenger',string="Passenger Name")
    contact_data = fields.Char(string="Contact Information")

    # Flight Information
    flight_ticket_id = fields.Many2one('ars.flight', string="Flight Number")
    flight_available_seats = fields.Integer(string='Available Seats',
                                            related='flight_ticket_id.available_seats')
    ticket_price = fields.Float(string='Price',default=0.0)

    @api.onchange('book_ref')
    def _onchange_flight_number(self):
        for rec in self:
            if rec.book_ref:
                rec.flight_ticket_id = rec.book_ref.flight_bk_id

    @api.model
    def create(self, vals_list):
        ticket = super(AircraftTicket, self).create(vals_list)

        for rec, val in zip(ticket, vals_list):
            # flight_ref = rec.flight_ticket_id.flight_no
            flight_ref = self.env['ars.flight'].browse(rec.flight_ticket_id.id).flight_no
            if flight_ref:
                rec['ticket_no'] = f'{flight_ref}/TK000{ticket.id}'
            else:
                rec['ticket_no'] = f'TK000{ticket.id}'
        return ticket
