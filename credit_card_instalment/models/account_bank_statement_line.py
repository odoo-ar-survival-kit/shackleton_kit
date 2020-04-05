# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    instalment_id = fields.Many2one(
        'account.journal.instalment',
        string='Instalment plan'
    )

    magnet_bar = fields.Char(
        'magnet bar'
    )
    card_number = fields.Char(
        'Card number'
    )
    tiket_number = fields.Char(
        'Tiket'
    )
    lot_number = fields.Char(
        'Lot'
    )
