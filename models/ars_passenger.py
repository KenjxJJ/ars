# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Passenger(models.Model):
    _name = 'ars.passenger'
    _description = 'ARS Passenger Information'
    _rec_name = 'ref'
    _order = 'create_date DESC'

    ref = fields.Char("Passenger ID")
    passenger_photo = fields.Image('Passenger Photo')
    fname = fields.Char("First Name")
    middlename = fields.Char("Middle Name")
    lname = fields.Char("Last Name")
    street = fields.Text("Street Address")
    city = fields.Char("City")
    country = fields.Char("Country")

    next_of_kin = fields.Char("Next Of Kin")
    nok_telephone = fields.Char("Next Of Kin\'s Phone Number")
    nok_address = fields.Text("Next Of Kin\'s Address")

    @api.model
    def create(self, vals):
        res = super(Passenger, self).create(vals)
        res['ref'] = 'ARS/PASSGR/' + str(res.id).zfill(4)
        return res

    def save_contact(self):
        return True
