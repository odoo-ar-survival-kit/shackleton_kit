# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

MAX_INSTALMENT = 24


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    card_type = fields.Selection(
        [('credit', 'credit'), ('debit', 'debit')],
    )

    accreditation_journal_id = fields.Many2one(
        'account.journal',
        string='accreditation to journal',
        domain=[('type', '=', 'bank')]
    )
    instalment_ids = fields.One2many(
        'account.journal.instalment',
        'journal_id',
        string='Instalments',
    )

    instalment_product_id = fields.Many2one(
        'product.product',
        string='Product to invoice'
    )

    def create_instalment_plan(self):
        self.ensure_one()
        if self.card_type=='debit':
            self.env['account.journal.instalment'].create({
                'name':'1',
                'instalment':1,
                'journal_id':self.id,
                'product_id':self.instalment_product_id.id

            })
        elif self.card_type=='credit':
            for i in range(1,MAX_INSTALMENT):
                self.env['account.journal.instalment'].create({
                    'name':str(i),
                    'instalment':i,
                    'journal_id':self.id,
                    'product_id':self.instalment_product_id.id

                })


class AccountJournalInstalment(models.Model):
    _name = 'account.journal.instalment'
    _description = 'amount to add for collection in installments'
    _order = "journal_id , instalment asc"

    @api.depends('name', 'journal_id', 'instalment')
    def _compute_name(self):
        for record in self:
            if record.name == '/' and len(record.journal_id) and record.instalment:
                record.name = "%s-%s" % (record.journal_id.name, record.instalment)

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        self.product_id = self.journal_id.product_id.id

    name = fields.Char(
        'Fantasy name',
        default='/'
    )

    journal_id = fields.Many2one(
        'account.journal',
        string='journal',
        domain=[('type', '=', 'banks')]
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
    card_type = fields.Selection(
        [('credit', 'credit'), ('debit', 'debit')],
        related="journal_id.card_type"
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
    @api.constrains('journal_id', 'instalment')
    def _check_instalment(self):
        for record in self:
            if record.journal_id.card_type == 'debit' and record.instalment > 1:
                raise ValidationError("Debit card has only 1 instalment plan")
            instalment = self.search([
                ('id','!=', record.id),
                ('journal_id', '=', record.journal_id.id),
                ('instalment', '=', record.instalment)
            ])
            if len(instalment):
                raise ValidationError("Instalment exist for this Journal")




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
