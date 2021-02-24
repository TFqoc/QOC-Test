# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import get_lang


class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def check_version(self):
        if not self.product_id:
            return
        version_tag = False
        version_number = -1
        for line in self.product_id.product_template_attribute_value_ids:
            if line.name.split(' ')[0] == 'Version':
                num = int(line.name.split(' ')[1])
                if num > version_number:
                    version_tag = line.name
                    version_number = num
        if version_number > self.product_id.version: #if we are still on an unapproved version
            return {
                'warning': {'title': "Warning", 'message': str(version_tag) + " of " + self.product_id.name + " is not yet approved. You will need to wait to manufacture this product until this version is approved",}
                }

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
                for line in eco.product_tmpl_id.attribute_line_ids:
                    if line.attribute_id.name == 'Version':
                        added = True
                        line.value_ids = [(4,version_id,0)]
                        break
                if not added:
                    eco.product_tmpl_id.attribute_line_ids = [(0,0,{
                        'attribute_id': attribute_id,
                        'product_tmpl_id': eco.product_tmpl_id,
                        'value_ids': [(4,version_id,0)],
                    })]
                # attach old bom to previous variant
                if eco.bom_id.product_tmpl_id.is_product_variant:
                    eco.bom_id.product_id = self.env['product.product'].search([
                        ('product_template_attribute_value_ids.name','=','Version ' + str(eco.bom_id.version)),
                        ('product_tmpl_id','=',eco.bom_id.product_tmpl_id.id)])[0]
                # attach new bom to previous variant
                eco.new_bom_id.product_id = self.env['product.product'].search([
                    ('product_template_attribute_value_ids.name','=','Version ' + str(eco.new_bom_id.version)),
                    ('product_tmpl_id','=',eco.new_bom_id.product_tmpl_id.id)])[0]
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
            # res = attr.copy(default={'name':'Version '+str(tag_number)})
            res = attr.value_ids.create({
                'name':'Version ' + str(tag_number),
                'attribute_id': attr_id,
            })
        return res.id, attr_id
            
### TODO Add to manifest
# class SaleConfigurator(models.Model):
#     _inherit = 'sale.product.configurator'

    # product_template_attribute_value_ids = fields.Many2many(
    #     'product.template.attribute.value', 'product_configurator_template_attribute_value_rel', 
    #     string='Attribute Values', readonly=True,compute='_newest_version')

    # def _newest_version(self):
    #     version = -1
    #     values = self.env['product.template.attribute.value'].search([('','','')])
    #     self.product_template_attribute_value_ids = [(6,0,[version])]

        