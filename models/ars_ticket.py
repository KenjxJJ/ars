from odoo import models, fields, api, _


class AircraftTicket(models.Model):
    _name = "ars.ticket"
    _description = "Ticket Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "ticket_no"

    ticket_no = fields.Char(string="Ticket No.")
    book_ref = fields.Many2one("ars.reservation", string="Booking ID")
    passenger_id = fields.Many2one('ars.passenger',string="Passenger Name")
    contact_data = fields.Char(string="Contact Information")

    # Flight Information
    flight_ticket_id = fields.Many2one('ars.flight', string="Flight Number")
    flight_available_seats = fields.Integer(string='Available Seats',
                                            related='flight_ticket_id.available_seats')
    ticket_price = fields.Float(string='Price',default=0.0)
