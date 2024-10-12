# -*- coding: utf-8 -*-

# import base64

from odoo import models, fields, api
# from odoo.tools import file_open


class Passenger(models.Model):
    _name = 'ars.passenger'
    _description = 'ARS Passenger Information'
    _rec_name = 'display_name'
    _order = 'create_date DESC'

    # @api.model
    # def _default_image(self):
    #     return base64.b64encode(file_open('path/to/passenger.png', 'rb').read())

    ref = fields.Char("Passenger ID")
    passenger_photo = fields.Image('Passenger Photo', max_width=128, max_height=128, compute_sudo=True)
    name = fields.Char(string='Passenger Name', default='/', copy=False, compute='_compute_display_name')
    fname = fields.Char("First Name", required=True)
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

    def _compute_display_name(self):
        for record in self:
            _name = ''
            if record.fname and record.lname:
                _name = record.fname if record.fname else _name
                _name = _name + ' ' + record.middlename if record.middlename else _name
                _name = _name + ' ' + record.lname if record.lname else _name
                record.display_name = _name
            else:
                record.display_name = record.fname

    def save_contact(self):
        return True
