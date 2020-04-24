# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class WebsiteWhatsapp(models.Model):
    _name = 'website.whatsapp'
    _description = 'Website whatsapp number'

    name = fields.Char(
        string='Number',
        required=True,
    )
    from_hour = fields.Float(
        string='from',
        required=True,
    )
    to_hour = fields.Float(
        string='to',
        required=True,
    )


class website(models.Model):
    _inherit = 'website'

    whatsapp_ids = fields.Many2many(
        'website.whatsapp',
        'website_whatsapp_rel',
        'website_id',
        'whatsapp_id',
        'Whatsapp numbers',
        #auto_join =True
    )

    whatsapp_active = fields.Char(
        string='whastme',
        compute="_compute_whatsapp_active"
    )
    whatsapp_inactive_url = fields.Char(
        string='whatsapp inactive url',
        default="/contact"
    )

    def _compute_whatsapp_active(self):

        now = datetime.now()  # to-do: website tz
        for website in self.sudo():
            float_now = float(now.hour) + (now.minute / 60)
            for phone in website.whatsapp_ids:
                if float_now <= phone.to_hour and float_now >= phone.from_hour:
                    website.whatsapp_active = phone.name
                    break
            if not website.whatsapp_active:
                website.whatsapp_active = ''


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    website_whatsapp_ids = fields.Many2many(
        related='website_id.whatsapp_ids',
        relation='website.whatsapp',
        readonly=False
    )
    website_whatsapp_inactive_url = fields.Char(
        string='Inactive URL',
        related="website_id.whatsapp_inactive_url",
        readonly=False
    )
