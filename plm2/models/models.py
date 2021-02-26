# -*- coding: utf-8 -*-
from collections import defaultdict
import json
import logging

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.tools.misc import get_lang
from odoo.addons.stock.models.stock_rule import ProcurementException

_logger = logging.getLogger(__name__)

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
                break
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
                v1 = False if version != 2 else eco.ensure_version_tag(1)[0]
                version_id, attribute_id = eco.ensure_version_tag(version)
                added = False
                for line in eco.product_tmpl_id.attribute_line_ids:
                    if line.attribute_id.name == 'Version':
                        added = True
                        line.value_ids = [(4,version_id,0)]
                        # Special case for first eco. We need to add version 1 tag so we get 2 total variants.
                        if v1:
                            line.value_ids = [(4,v1,0)]
                        break
                if not added:
                    eco.product_tmpl_id.attribute_line_ids = [(0,0,{
                        'attribute_id': attribute_id,
                        'product_tmpl_id': eco.product_tmpl_id,
                        'value_ids': [(4,version_id,0)] if not v1 else [(4,version_id,0),(4,v1,0)],
                    })]
                # attach old bom to previous variant
                if eco.bom_id.product_tmpl_id.is_product_variant or v1:
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
            res = attr.value_ids.create({
                'name':'Version ' + str(tag_number),
                'attribute_id': attr_id,
                'sequence': -tag_number, #so the newest version has the lowest sequence.
            })
        return res.id, attr_id

    # @api.onchange('product_tmpl_id')
    # def onchange_product_tmpl_id(self):
    #     if self.product_tmpl_id.bom_ids:
    #         self.bom_id = self.product_tmpl_id.bom_ids.ids[0]

class MRPbom(models.Model):
    _inherit = 'mrp.bom'

    def apply_new_version(self):
        """ Put old BoM as deprecated """
        MrpEco = self.env['mrp.eco']
        for new_bom in self:
            new_bom.write({'active': True})
            # Move eco's into rebase state which is in progress state.
            ecos = MrpEco.search(['|',
                    ('bom_id', '=', new_bom.previous_bom_id.id),
                    ('current_bom_id', '=', new_bom.previous_bom_id.id),
                    ('new_bom_id', '!=', False),
                    ('new_bom_id', '!=', new_bom.id),
                    ('state', 'not in', ('done', 'new'))])
            ecos.write({'state': 'rebase', 'current_bom_id': new_bom.id})
            # Change old bom of eco which is in draft state.
            draft_ecos = MrpEco.search(['|',
                ('bom_id', '=', new_bom.previous_bom_id.id),
                ('current_bom_id', '=', new_bom.previous_bom_id.id),
                ('new_bom_id', '=', False)])
            draft_ecos.write({'bom_id': new_bom.id})
            # Deactivate previous revision of BoM
            # new_bom.previous_bom_id.write({'active': False})
        return True
            
# class SaleConfigurator(models.TransientModel):
#     _inherit = 'sale.product.configurator'

#     product_template_attribute_value_ids = fields.Many2many(
#         'product.template.attribute.value', 'product_configurator_template_attribute_value_rel', 
#         string='Attribute Values', readonly=True,compute='_newest_version')

#     def _newest_version(self):
#         version_id = -1
#         values = self.env['product.template.attribute.value'].search([('product_attribute_value_id','=','Version')])
#         for v in values:
#             if v.name == "Version " + str(self.project_template_id.version):
#                 version_id = v.id
#                 break
#         self.product_template_attribute_value_ids = [(6,0,[version_id])]
class Procurements(models.Model):
    _name = 'delayed.procurement'
    _description = 'Delayed Procurement'

    dict_string = fields.Char(readonly=True)

    def get_dict(self):
        return json.loads(self.dict_string)

    def try_manufacture(self):
        procurements  = {}
        for p in self:
            procurements.update(self.get_dict())
        self.unlink(self)
        self.env['stock.rule']._run_manufacture(procurements)

class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_manufacture(self, procurements):
        productions_values_by_company = defaultdict(list)
        errors = []
        _logger.debug(procurements)
        for procurement, rule in procurements:
            # Don't manufacture product if it's version is too new
            version = 0
            for p in procurement.product_id.product_template_attribute_value_ids:
                if p.name.split(' ')[0] == "Version":
                    version = int(p.name.split(' ')[1])
                    # Create a stored procurement record
                    self.env['delayed.procurement'].create({'dict_string':str({str(procurement), str(rule)})})
                    break
            if version > procurement.product_id.product_tmpl_id.version:
                continue
            # End my code
            bom = self._get_matching_bom(procurement.product_id, procurement.company_id, procurement.values)
            if not bom:
                msg = _('There is no Bill of Material of type manufacture or kit found for the product %s. Please define a Bill of Material for this product.') % (procurement.product_id.display_name,)
                errors.append((procurement, msg))

            productions_values_by_company[procurement.company_id.id].append(rule._prepare_mo_vals(*procurement, bom))

        if errors:
            raise ProcurementException(errors)

        for company_id, productions_values in productions_values_by_company.items():
            # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
            productions = self.env['mrp.production'].with_user(SUPERUSER_ID).sudo().with_company(company_id).create(productions_values)
            self.env['stock.move'].sudo().create(productions._get_moves_raw_values())
            self.env['stock.move'].sudo().create(productions._get_moves_finished_values())
            productions._create_workorder()
            productions.filtered(lambda p: p.move_raw_ids).action_confirm()

            for production in productions:
                origin_production = production.move_dest_ids and production.move_dest_ids[0].raw_material_production_id or False
                orderpoint = production.orderpoint_id
                if orderpoint:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={'self': production, 'origin': orderpoint},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
                if origin_production:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={'self': production, 'origin': origin_production},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        return True