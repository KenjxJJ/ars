# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AirportEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'ARS Employee Information'

    crew_id = fields.Many2one('ars.aircraft', string='Crew Member')

    @api.model
    def create(self, vals):
        ars_tag = self.env['hr.employee.category'].search([('name', '=', 'ARS')], limit=1)
        if ars_tag:
            if 'category_ids' in vals:
                vals['category_ids'] = [(4, ars_tag.id)] + vals.get('category_ids', [])
            else:
                vals['category_ids'] = [(6, 0, [ars_tag.id])]

        return super(AirportEmployee, self).create(vals)

