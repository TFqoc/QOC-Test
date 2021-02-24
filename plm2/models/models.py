# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import get_lang


class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    version = fields.Integer()

    @api.onchange('version')
    def version_change(self):
        if not self.product_id:
            return
        if self.version < 1:
            self.version = 1
        elif self.version > self.product_id.version:
            valid = False
            for eco in self.product_id.eco_ids:
                if eco.new_bom_revision is self.version:
                    valid = True
            if not valid:
                self.version = self.product_id.version
        if self.version > self.product_id.version: #if we are still on an unapproved version
            return {
                'warning': {'title': "Warning", 'message': "Version " + str(self.version) + " of " + self.product_id.name + " is not yet approved. You will need to wait to manufacture this product until this version is approved",}
                }
        

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        # Copy over the version field as well
        self.version = self.product_id.version
        
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result

class Product(models.Model):
    _inherit = 'product.template'

    version = fields.Integer('Version', default=1, readonly = True, help="The current version of the product.")

class Eco(models.Model):
    _inherit = 'mrp.eco'

    def action_new_revision(self):
        IrAttachment = self.env['ir.attachment']
        for eco in self:
            if eco.type in ('bom', 'both'):
                eco.new_bom_id = eco.bom_id.copy(default={
                    'version': eco.bom_id.version + 1,
                    'active': False,
                    'previous_bom_id': eco.bom_id.id,
                })
                attachments = IrAttachment.search([('res_model', '=', 'mrp.bom'),
                                                   ('res_id', '=', eco.bom_id.id)])
                for attachment in attachments:
                    attachment.copy(default={'res_id':eco.new_bom_id.id})
            if eco.type in ('routing', 'both'):
                eco.new_routing_id = eco.routing_id.copy(default={
                    'version': eco.routing_id.version + 1,
                    'active': False,
                    'previous_routing_id': eco.routing_id.id
                }).id
                attachments = IrAttachment.search([('res_model', '=', 'mrp.routing'),
                                                   ('res_id', '=', eco.routing_id.id)])
                for attachment in attachments:
                    attachment.copy(default={'res_id':eco.new_routing_id.id})
            if eco.type == 'both':
                eco.new_bom_id.routing_id = eco.new_routing_id.id
                for line in eco.new_bom_id.bom_line_ids:
                    line.operation_id = eco.new_routing_id.operation_ids.filtered(lambda x: x.name == line.operation_id.name).id
            # duplicate all attachment on the product
            if eco.type in ('bom', 'both', 'product'):
                attachments = self.env['mrp.document'].search([('res_model', '=', 'product.template'), ('res_id', '=', eco.product_tmpl_id.id)])
                for attach in attachments:
                    attach.copy({'res_model': 'mrp.eco', 'res_id': eco.id})
            # add new variant to product
            if eco.type in ('product','bom','both'):
                version = eco.bom_id.version + 1
                version_id, attribute_id = eco.ensure_version_tag(version)
                added = False
                while True:
                    for line in eco.product_tmpl_id.attribute_line_ids:
                        if line.attribute_id.name == 'Version':
                            added = True
                            # line.write({'product_template_value_ids',(4,version_id,0)})
                            line.product_template_value_ids = [(4,version_id,0)]
                            break
                    if not added:
                        eco.product_tmpl_id.write({'attribute_line_ids':(0,0,{
                            'attribute_id': attribute_id,
                            'product_tmpl_id': eco.product_tmpl_id,
                        })})
                    else:
                        break
        self.write({'state': 'progress'})

    def ensure_variant(self):
        # check if attribute exists. If not, create it
        attr = self.env['product.attribute'].search([('name','=','Version')])
        if not attr:
            #create record for the attribute
            attr = self.env['product.attribute'].create({
                'name':'Version',
                'display_type':'select',
                'create_variant':'always',
            })
        return attr.id

    def ensure_version_tag(self, tag_number):
        attr_id = self.ensure_variant()
        # check if version tag exists. If not, create it
        attr = self.env['product.attribute'].browse(attr_id)
        res = False
        if attr.value_ids:#in case the list is empty
            for val in attr.value_ids:
                if int(val.name.split(' ')[1]) == tag_number:
                    res = val
                    break
        if not res:
            res = attr.copy(default={'name':'Version '+str(tag_number)})
        return res.id, attr_id
            
        