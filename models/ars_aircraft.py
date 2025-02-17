# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Aircraft(models.Model):
    _name = "ars.aircraft"
    _description = "Aircraft Information"

    name = fields.Char("Aircraft Number")
    model = fields.Char(string='Model', required=True)
    manufacturer = fields.Char(string='Manufacturer')
    serial_number = fields.Char(string='Serial Number')
    seating_capacity = fields.Integer(string='Total Seating Capacity')
    business_class_seats = fields.Integer(string='Business Class Seats')
    economy_class_seats = fields.Integer(string='Economy Class Seats')

    current_location_id = fields.Many2one('ars.airport', string='Current Location')
    crew_requirement = fields.Integer(string='Minimum Crew Required')
    assigned_flights = fields.One2many('ars.flight', 'aircraft_id', string='Assigned Flights')
    fuel_capacity = fields.Float(string='Fuel Capacity (Liters)')
    range = fields.Float(string='Range (Kilometers)')

    status = fields.Selection([
        ('active', 'Active'),
        ('in_maintenance', 'In Maintenance'),
        ('retired', 'Retired')
    ], string='Status', default='active')