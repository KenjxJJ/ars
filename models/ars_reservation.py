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
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    invoice_id = fields.Many2one('account.move', domain=[('move_type','=','out_invoice')])
    payment_state = fields.Selection(related='invoice_id.payment_state', store=True)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('save', 'Set'),
        ('invoice', 'Invoiced'),
    ], default='draft', string="Booking Status")

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
    def _default_account(self):
        acc = self.env['account.account'].search(
            [('account_type', '=', 'income')], limit=1)
        return acc.id

    def set_booking(self):
        for rec in self:
            self.create_partner()
            rec.write({'status': 'save'})

    def set_draft(self):
        for rec in self:
            rec.write({'status': 'draft'})

    def create_partner(self):
        for rec in self:
            partner_obj = self.env['res.partner']

            if rec.passenger_id:
                new_partner = partner_obj.create({
                    'name': rec.passenger_id.display_name,
                    'is_company': False,
                    'email': rec.passenger_id.email,
                    'mobile': rec.passenger_id.mobile,
                    'street': rec.passenger_id.street,
                    'category_id': [(4, rec.passenger_id.id)],
                    'customer_rank': 1,
                })
                rec.partner_id = new_partner

    def action_create_invoice(self):
        for booking in self:
            invoiced_services = []
            for ticketinfo in booking.ticket_ids:
                info = {
                    'name': f'Ticket No: {ticketinfo.ticket_no}\n Passenger: {ticketinfo.passenger_id.display_name}\n\n'
                            f'Contact Info: {ticketinfo.contact_data}',
                    'price_unit': ticketinfo.ticket_price,
                    'quantity': 1,
                    'account_id': booking._default_account()
                }
                invoiced_services.append((0, 0, info))

            context = dict({
                'create': False,
                'default_move_type': 'out_invoice',
            })

            inv_vals = {
                'partner_id': booking.partner_id.id,
                'invoice_date': booking.book_datetime.strftime('%Y-%m-%d'),
                'invoice_date_due': booking.book_datetime.strftime('%Y-%m-%d'),
                'invoice_line_ids': invoiced_services,
                'payment_reference': f"Booking Reference %s for %s" % (booking.name, booking.partner_id.name),
                'move_type': 'out_invoice',
               }

            invoice = self.env['account.move'].create(inv_vals)
            booking.write({
                'invoice_id': invoice.id,
                'status': 'invoice',
            })

            return {
                "name": "Booking Invoice %s" % booking.name,
                "view_type": "form",
                "res_model": "account.move",
                "view_id": False,
                "res_id": booking.invoice_id.id,
                "view_mode": "form",
                "type": "ir.actions.act_window",
                "context": context
            }
