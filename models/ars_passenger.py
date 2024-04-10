# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Passenger(models.Model):
    _name = 'ars.passenger'
    _description = 'ARS Passenger Information'
    _rec_name = 'ref'
    _order = 'create_date DESC'

    ref = fields.Char("Passenger ID")
    fname = fields.Char("First Name")
    lname = fields.Char("Last Name")
