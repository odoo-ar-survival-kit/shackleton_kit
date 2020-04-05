# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class credit_card_instalment_invoice(models.Model):
#     _name = 'credit_card_instalment_invoice.credit_card_instalment_invoice'
#     _description = 'credit_card_instalment_invoice.credit_card_instalment_invoice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
