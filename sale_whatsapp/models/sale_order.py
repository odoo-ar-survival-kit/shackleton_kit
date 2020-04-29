# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import uuid


class SaleOrder(models.Model):
    _inherit = 'sale.order'

 
    def open_whapp(self):
        self.ensure_one()
        saleText =_("Your%20sale%20order")
        if self.partner_id.mobile:
            url = 'https://api.whatsapp.com/send?phone=%s/&text=%s%%20%s' % (
                self.partner_id.mobile, saleText ,self.access_url)

            return {
                'name': 'open_whapp',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'what',
                'url': url
            }
