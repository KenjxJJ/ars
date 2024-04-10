# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Aircraft(models.Model):
    _name = "ars.aircraft"
    _description = "Aircraft Information"

    name = fields.Char("Aircraft Number")
