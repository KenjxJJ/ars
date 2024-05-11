from odoo import models, fields, api, _


class AircraftFlight(models.Model):
    _name = "ars.flight"
    _description = "Aircraft Flight Information"

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
