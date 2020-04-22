from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    #state = fields.Selection(selection_add=[('payment', 'Payment in process')])

    def action_invoice_draft_register_payment(self):
        return self.env['account.payment']\
            .with_context(active_ids=self.ids, active_model='account.move', active_id=self.id)\
            .action_register_draft_payment()
        