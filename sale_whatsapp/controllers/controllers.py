# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class SaleWhatsapp(http.Controller):
    @http.route(['/saleorder/<uuid:unic>'], type='http', auth="public", website=True)
    def sale_order_access(self, unic, **post):

        order_id = request.env['crm.lead'].sudo().search(
            [('unic_uuid', '=', unic)], limit=1)
        report_obj = request.env['report']

        if len(order_id):
	        if order_id.state not in ['draft','cancel']:
	            html = report_obj.sudo().get_html( order_id, 'sale.report_saleorder')
	            return request.make_response(html)
        return 'none'

    @http.route(['/lead/<uuid:unic>/pdf'], type='http', auth="public", website=True)
    def crm_lead_access_pdf(self, unic, **post):


        order_id = request.env['crm.lead'].sudo().search(
            [('unic_uuid', '=', unic)], limit=1)
        report_obj = request.env['report']


        if len(order_id):
            if order_id.state == 'sent':
                pdf = report_obj.sudo().get_pdf(order_id, 'sale.report_saleorder')
                pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
                return request.make_response(pdf, headers=pdfhttpheaders)
        return 'none'
