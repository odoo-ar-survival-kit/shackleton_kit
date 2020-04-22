# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

MAX_INSTALMENT = 24


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    card_type = fields.Selection(
        [('credit', 'credit'), ('debit', 'debit')],
    )

    card_partner_id = fields.Many2one(
        'account.journal',
        string='Card Partner',
    )
    instalment_ids = fields.One2many(
        'account.card.instalment',
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


class AccountCardInstalment(models.Model):
    _inherit = 'account.card.instalment'
    _order = "journal_id , instalment asc"

    @api.depends('name', 'journal_id', 'instalment')
    def _compute_name(self):
        for record in self:
            if record.name == '/' and len(record.journal_id) and record.instalment:
                record.name = "%s-%s" % (record.journal_id.name, record.instalment)

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        self.product_id = self.journal_id.product_id.id

    journal_id = fields.Many2one(
        'account.journal',
        string='journal',
        domain=[('type', '=', 'banks')]
    )
    card_type = fields.Selection(
        [('credit', 'credit'), ('debit', 'debit')],
        related="journal_id.card_type"
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

