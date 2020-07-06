# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from lxml import etree, builder
from odoo.addons.http_routing.models.ir_http import slugify
import re
from odoo.tools.safe_eval import safe_eval


import logging
_logger = logging.getLogger(__name__)

MY_NAMESPACES = {'g': 'http://base.google.com/ns/1.0',
                 None: 'http://base.google.com/ns/1.0'}
CLEANTAG = re.compile('<.*?>')


class productGoogleProducttype(models.Model):
    _name = 'product.google.producttype'
    _description = 'Google_Product Taxonomy Version'

    tax_id = fields.Integer(
        string='Taxonomy Id',
    )
    name = fields.Char(
        string='Tax Description',
    )


class productTemplate(models.Model):
    _inherit = 'product.template'

    producttype_id = fields.Many2one(
        'product.google.producttype',
        string='Google Taxonomy',
    )


class productCategory(models.Model):
    _inherit = 'product.category'

    producttype_id = fields.Many2one(
        'product.google.producttype',
        string='Google Taxonomy',
    )


class product_google_feed(models.Model):
    _name = 'product.google.feed'
    _description = 'Product google feed'

    name = fields.Char(
        string='feed',
        size=64,
        required=False,
        readonly=False,
    )
    website_id = fields.Many2one(
        'website',
        string='website',
        required=False,
    )
    base_url = fields.Char(
        string='base url',
        default='shop/product/'
    )

    slug = fields.Char(
        string='slug',
    )

    domain = fields.Text(
        string='domain',
        default="[('website_published','=',True)]",
    )

    context = fields.Text(
        string='context',
        default="{'pricelist':1}"
    )

    producttype_id = fields.Many2one(
        'product.google.producttype',
        string='Google Taxonomy',
    )


    active = fields.Boolean(
        string='Active',
        default=True,
    )
    limit = fields.Integer(
        string='limit',
        default=100
    )

    @api.onchange('name')
    def _compute_slug(self):
        for feed in self:
            feed.slug = slugify(self)

    def make_xml(self):
        self.ensure_one()
        domain = safe_eval(self.domain)
        context = safe_eval(self.context)

        product_ids = self.env['product.template'].sudo().with_context(
            context).search(domain, limit=self.limit)

        E = builder.ElementMaker()
        rss = etree.Element("rss", nsmap=MY_NAMESPACES, version="2.0")

        channel = E.channel(E.title(self.name), E.link(
            self.website_id.domain), E.description(self.name))
        rss.append(channel)

        for product_id in product_ids:
            item = E.item()
            sku = etree.Element('{%s}id' % MY_NAMESPACES['g'])
            sku.text = product_id['default_code'] if  product_id['default_code'] else 'p-%i'%product_id['default_code'] 
            item.append(sku)

            if product_id['barcode']:
                gtin = etree.Element('{%s}gtin' % MY_NAMESPACES['g'])
                gtin.text = product_id['barcode']
                item.append(gtin)

            if product_id['default_code']:
                mpn = etree.Element('{%s}mpn' % MY_NAMESPACES['g'])
                mpn.text = product_id['default_code']
                item.append(mpn)

            title = etree.Element('title')
            title.text = product_id['name']
            item.append(title)

            description = etree.Element('description')
            if product_id['description']:
                description.text = re.sub(
                    CLEANTAG, '', product_id['description'])
            else:
                description.text = product_id['name']
            item.append(description)

            availability = etree.Element(
                '{%s}availability' % MY_NAMESPACES['g'])
            if product_id.qty_available > 0:
                availability.text = 'in stock'
            else:
                availability.text = 'preorder'
            item.append(availability)

            brand = etree.Element('{%s}brand' % MY_NAMESPACES['g'])
            if 'product_brand_id' in product_id and len(product_id.product_brand_id):
                brand.text = product_id.product_brand_id.name
            else:
                brand.text = self.website_id.name
            item.append(brand)


            link = etree.Element('link')
            link.text = "%s/%s%s" % (self.website_id.domain,
                                     self.base_url, slugify(product_id))
            item.append(link)


            price = etree.Element('{%s}price' % MY_NAMESPACES['g'])

            # to-do: calcular impuestos y currency
            if 'pack' in  product_id and product_id.pack:
                price.text = "%.2f %s" % (product_id._price_get(
                    [product_id])[product_id.id] ,self.env.company.currency_id.name)

            else:
                #to-do tax ? product_id['list_price']
                price.text = "%.2f %s" % (product_id['list_price'] ,self.env.company.currency_id.name)

            item.append(price)

            if product_id['image']:
                image_link = etree.Element('{%s}image_link' % MY_NAMESPACES['g'])
                image_link.text = '%s/web/image/product.product/%i/image/' % (
                    self.website_id.domain, product_id.id)
                item.append(image_link)
            else :
                pass
                #add default IMG

            #additional_image_link
            condition = etree.Element('{%s}condition' % MY_NAMESPACES['g'])
            condition.text = 'new'
            item.append(condition)

            if not product_id['default_code'] or not product_id['barcode']: 
                identifier_exists = etree.Element(
                    '{%s}identifier_exists' % MY_NAMESPACES['g'])
                identifier_exists.text = 'no'
                item.append(identifier_exists)

            google_product_category = etree.Element(
                '{%s}google_product_category' % MY_NAMESPACES['g'])

            if len(product_id.producttype_id):
                google_product_category.text = str(
                    product_id.producttype_id.tax_id)
            elif (len(product_id.categ_id.producttype_id)):
                google_product_category.text = str(
                    product_id.categ_id.producttype_id.tax_id)
            else:
                google_product_category.text = str(self.producttype_id.tax_id)
            item.append(google_product_category)

            channel.append(item)

        return etree.tostring(rss, xml_declaration=True, encoding="utf-8", pretty_print=True)

#        headers=[('Content-Type', 'application/json; charset=utf-8')]
