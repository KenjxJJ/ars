# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AirportReservation(models.Model):
    _name = 'ars.airport'
    _description = 'Airports Information'

    name = fields.Char("Reservation Number")
