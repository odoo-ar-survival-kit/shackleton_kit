# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class google_feed(http.Controller):

    @http.route('/google_feed/<string:slug>', auth='public')
    def google_feed(self, slug, page=0, **kw):
        feed_id = request.env['product.google.feed'].sudo().search(
            [('slug', '=', slug)], limit=1)

        if len(feed_id):
            return request.make_response(feed_id.sudo().make_xml(), headers=[('Content-type', 'text/xml')])
        return  ''
