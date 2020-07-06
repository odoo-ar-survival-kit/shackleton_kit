# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

MAX_INSTALMENT = 24


class AccountCardInstalment(models.Model):
    _name = 'account.card.instalment'
    _description = 'amount to add for collection in installments'

    name = fields.Char(
        'Fantasy name',
        default='/'
    )
    instalment = fields.Integer(
        string='instalment plan',
        min=1,
        max=MAX_INSTALMENT,
        help='Number of instalment, less than %s' % str(MAX_INSTALMENT + 1)
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product to invoice'
    )
    amount = fields.Float(
        string='Fix amount'
    )
    coefficient = fields.Float(
        string='coefficient',
        help='Value to multiply the amount'
    )

    active = fields.Boolean(
        'Active',
        default=True
    )
    ctf = fields.Float(
        string='C.T.F.'
    )
    tea = fields.Float(
        string='TEA'
    )
    accreditation_id = fields.Many2one(
        'account.journal.instalment.accreditation',
        string='Accreditation method',
    )


class AccountJournalInstalmentAccreditation(models.Model):
    _name = 'account.journal.instalment.accreditation'
    _description = 'bank accreditation method'

    name = fields.Char(
        string='Name',
    )
    accreditation_method = fields.Selection(
        [('after_days', 'after X days'),
         ('next_day_number', 'next day number'),
         ('first_dayweek', 'First day off next month')],
        string='Accreditation method',
    )
    accreditation_param = fields.Char(
        string='accreditation param',
    )
    accreditation_closing_param = fields.Char(
        string='accreditation closing param',
    )
