from odoo import models, fields, api, _


class AircraftFlight(models.Model):
    _name = "ars.flight"
    _description = "Aircraft Flight Information"

    flight_no = fields.Char("Flight Number")
