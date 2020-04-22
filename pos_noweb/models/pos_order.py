from odoo import api, fields, models, _
from odoo.tools import formatLang
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):

    _inherit = "pos.order"
    invoice_group = fields.Boolean(related="config_id.module_account", readonly=True)

    @api.model
    def default_get(self, vals):

        res = super(PosOrder, self).default_get(
            vals + ['company_id', 'currency_id'])

        res['company_id'] = self.env.company.id
        session_id = self.env['pos.session'].search([
            ('state', '=', 'opened'),
            ('config_id.company_id', '=', self.env.company.id)],
            limit=1
        )
        if not len(session_id):
            raise ValidationError(_('No opened session'))

        res['session_id'] = session_id.id
        res['amount_paid'] = 0.0
        res['amount_return'] = 0.0
        res['pricelist_id'] = session_id.config_id.pricelist_id.id
        res['fiscal_position_id'] = session_id.config_id.default_fiscal_position_id.id

        res['invoice_group'] = session_id.config_id.module_account
        return res

    @api.model
    def _complete_values_from_session(self, session, values):
        values = super(PosOrder, self)._complete_values_from_session(
            session, values)
        if 'invoice_group' in values:
            del values['invoice_group']
        _logger.info(values)

        return values
