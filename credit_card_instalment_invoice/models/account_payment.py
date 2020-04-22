from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    instalment_id = fields.Many2one(
        'account.journal.instalment',
        string='Instalment plan'
    )

    card_type = fields.Selection(
        [('credit', 'credit'), ('debit', 'debit')],
        related="journal_id.card_type"
    )

    magnet_bar = fields.Char(
        'magnet bar'
    )
    card_number = fields.Char(
        'Card number'
    )
    tiket_number = fields.Char(
        'Tiket number'
    )
    lot_number = fields.Char(
        'Lot number'
    )
    fee = fields.Float(
        string='Fee',
        default=0,
    )
    total_amount = fields.Float(
        string='total amount',
        default=0,
    )

    draft_invoice_ids = fields.Many2many('account.move', 'account_draft_invoice_payment_rel', 'payment_id', 'invoice_id', string="Invoices", copy=False, readonly=True,
                                         help="""Technical field containing the invoice for which the payment has been generated.
                                """)

    @api.onchange('magnet_bar')
    def _onchange_magnet_bar(self):
        if self.magnet_bar:
            try:
                track1, track2 = self.magnet_bar.split(';')
                cardnumber, name, data = track1.split('^')
                # to-do: add chksum
                self.card_number = cardnumber
            except ValueError:
                raise ValidationError(_('Could not parse track'))

    def action_register_draft_payment(self):
        active_ids = self.env.context.get('active_ids')

        if len(active_ids) != 1:
            raise ValidationError(_('Not Implemented'))
        if not active_ids:
            return ''
        draft_invoices = self.env['account.move'].browse(active_ids)
        ##amount = self._compute_payment_amount(draft_invoices, draft_invoices[0].currency_id, draft_invoices[0].journal_id,  fields.Date.today())
        amount = 0
        self.env.context = dict(self.env.context)
        if draft_invoices[0].is_inbound():
            payment_type = 'inbound'
        else:
            payment_type = 'outbound'
        partner_id = draft_invoices[0].partner_id.id
        # to-do : default Get
        self.env.context.update({'default_partner_id': partner_id, 'default_payment_type': payment_type, 'active_id': False,
                                 'active_ids': False, 'default_draft_invoice_ids': [(6, 0, draft_invoices.ids)], 'default_amount': amount})
        return {
            'name': _('Register Payment'),
            'res_model': len(active_ids) == 1 and 'account.payment' or 'account.payment.register',
            'view_mode': 'form',
            'view_id': len(active_ids) != 1 and self.env.ref('account.view_account_payment_form_multi').id or self.env.ref('account.view_account_payment_invoice_form').id,
            'context': self.env.context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def draft_post(self):

        for rec in self:
            if rec.fee != 0.0:

                if len(rec.draft_invoice_ids):
                    fee_invoice_id = False
                    # to-do usar filterd
                    for invoice_id in rec.draft_invoice_ids:
                        if invoice_id == 'draft':
                            fee_invoice_id = invoice_id
                            break
                    if not fee_invoice_id:
                        raise ValidationError(_('Invoices not Draft'))
                    fee_invoice_id.invoice_line_ids = [(0, 0, {
                        'product_id': rec.instalment_id.product_id.id,
                        'quantity': 1,
                        'price_unit': rec.fee,
                        #'tax_ids'[:(6,0,[rec.instalment_id.product_id.id.tax_ids.ids])]
                        #'account_id'
                    })]
                rec.amount = rec.amount + rec.fee

        return super(AccountPayment, self).post()

    def post(self):
        for rec in self:
            if rec.fee != 0.0:
                if len(rec.invoice_ids):
                    fee_invoice_id = False
                    # to-do usar filterd
                    for invoice_id in rec.invoice_ids:
                        if invoice_id == 'draft':
                            fee_invoice_id = invoice_id
                            break

                    if not fee_invoice_id:
                        fee_invoice_id = self.env['account.move'].create(
                            {
                                'type': rec.invoice_ids[0].type,
                                'journal_id': rec.invoice_ids[0].journal_id.id,
                                'partner_id': rec.invoice_ids[0].partner_id.id,
                                'invoice_user_id': rec.invoice_ids[0].invoice_user_id.id,
                                'team_id': rec.invoice_ids[0].team_id.id,
                                #'invoice_incoterm_id': rec.invoice_ids[0].incoterm_id.id,

                            }
                        )
                    fee_invoice_id.invoice_line_ids = [(0, 0, {
                        'product_id': rec.instalment_id.product_id.id,
                        'quantity': 1,
                        'price_unit': rec.fee,
                        #'tax_ids'[:(6,0,[rec.instalment_id.product_id.id.tax_ids.ids])]
                        #'account_id'
                    })]

                    rec.invoice_ids = [(4, fee_invoice_id.id)]
                    if fee_invoice_id.state == 'draft':
                        fee_invoice_id.action_post()
                rec.amount = rec.amount + rec.fee

        return super(AccountPayment, self).post()

    @api.onchange('instalment_id')
    def change_instalment_id(self):
        self.ensure_one()
        if len(self.instalment_id):
            if self.instalment_id.coefficient:
                tax_amount = 0
                if self.instalment_id.product_id.taxes_id:

                    if len(self.fee_id.product_id.taxes_id) > 1:
                        raise ValidationError(
                            'El plan de cuotas tiene multiples impuestos configurados')
                    tax_amount = self.fee_id.product_id.taxes_id.amount

                #self.fee = self.instalment_id.fee
                self.fee = self.amount * \
                    self.instalment_id.coefficient * (1 + tax_amount / 100)
                self.total_amount = self.amount + self.fee
                """
                vals = {
                    'fee': self.fee,
                    'fee': self.fee,
                    'total_amount': self.total_amount,
                    }
                self.write(vals)
                """

            else:
                self.fee = 0
                self.total_amount = self.amount
        else:
            self.fee = 0
            self.total_amount = self.amount
"""
account.move
    def action_invoice_register_payment(self):
        return self.env['account.payment']\
            .with_context(active_ids=self.ids, active_model='account.move', active_id=self.id)\
            .action_register_payment()
        """
