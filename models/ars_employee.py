# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AirportEmployee(models.Model):
    _name = 'ars.employee'
    _description = 'ARS Employee Information'

    ref = fields.Char("Employee Number")
    fname = fields.Char("First Name")
    lname = fields.Char("Last Name")
