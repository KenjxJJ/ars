# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AirportReservation(models.Model):
    _name = 'ars.reservation'
    _description = 'Airport Reservation (Booking)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    name = fields.Char(string="Booking Ref", help="Reservation Number", default='/', readonly=1)
    book_datetime = fields.Datetime(string="Booking Date")

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', compute='_compute_company_currency')
    total_amount = fields.Monetary(string="Total Amount", compute='_compute_total_ticket_prices',
                                   store=True)

    # Tickets
    ticket_ids = fields.One2many(comodel_name="ars.ticket",
                                 inverse_name="book_ref",
                                 string="Tickets", help="Tickets as per the booking")

    # Flights
    flight_bk_id = fields.Many2one('ars.flight', string='Selected Flight')
    passenger_id = fields.Many2one('ars.passenger', string='Booked by')

    status = fields.Selection([('draft', 'Draft'), ('save', 'Set')], default='draft', string="Booking Status")

    @api.depends('company_id')
    def _compute_company_currency(self):
        for rec in self:
            if rec.company_id:
                rec.currency_id = rec.company_id.currency_id
            else:
                curr = self.env['res.currency'].search([], limit=1)
                rec.currency_id = curr.id

    @api.depends('ticket_ids')
    def _compute_total_ticket_prices(self):
        for rec in self:
            rec.total_amount = sum(rec.ticket_ids.mapped('ticket_price')) if rec.ticket_ids else 0.0


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('/')) == _('/'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'ars.reservation')

                # Set the default booking date if not provided
            if not vals.get('book_datetime'):
                vals['book_datetime'] = fields.Datetime.now()

        return super().create(vals_list)

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------

    def set_booking(self):
        for rec in self:
            rec.write({'status': 'save'})

    def set_draft(self):
        for rec in self:
            rec.write({'status': 'draft'})
