# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api
from odoo.tools import file_open


class Passenger(models.Model):
    _name = 'ars.passenger'
    _description = 'ARS Passenger Information'
    _rec_name = 'ref'
    _order = 'create_date DESC'

    # @api.model
    # def _default_image(self):
    #     return base64.b64encode(file_open('path/to/passenger.png', 'rb').read())

    ref = fields.Char("Passenger ID")
    passenger_photo = fields.Image('Passenger Photo', max_width=128, max_height=128, compute_sudo=True)
    fname = fields.Char("First Name")
    middlename = fields.Char("Middle Name")
    lname = fields.Char("Last Name")
    email = fields.Char("Email")
    mobile = fields.Char("Mobile")
    street = fields.Text("Street Address")
    city = fields.Char("City")
    country = fields.Char("Country")

    next_of_kin = fields.Char("Next Of Kin")
    nok_telephone = fields.Char("Next Of Kin\'s Phone Number")
    nok_address = fields.Text("Next Of Kin\'s Address")
    active = fields.Boolean("Active", default=True)

    @api.model
    def create(self, vals):
        res = super(Passenger, self).create(vals)
        for passenger in res:
            passenger['ref'] = 'ARS/PASSGR/' + str(res.id).zfill(4)
        return res

    def save_contact(self):
        return True
