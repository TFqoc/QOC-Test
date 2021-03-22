# -*- coding: utf-8 -*-
from collections import defaultdict
from random import randint

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class RMA(models.Model):
    _name = 'rma.rma'
    _description = 'rma.rma'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    _sql_constraints = [
        ('name', 'unique (name)', 'The name of the Repair Order must be unique!'),
    ]

    production_id = fields.Many2one('mrp.production', readonly=True)
    name = fields.Char(
        'RMA Reference',
        default='/',
        copy=False, required=True, readonly=True)
        # states={'confirmed': [('readonly', True)]})
    sale_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True)
    product_qty = fields.Float(
        'Product Quantity',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    product_uom = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        readonly=True, required=True, states={'draft': [('readonly', False)]}, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, states={'confirmed': [('readonly', True)]}, check_company=True, change_default=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.')
    address_id = fields.Many2one(
        'res.partner', 'Delivery Address',
        domain="[('parent_id','=',partner_id)]", check_company=True,
        states={'confirmed': [('readonly', True)]})
    default_address_id = fields.Many2one('res.partner', compute='_compute_default_address_id')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Repair'),
        ('ready', 'Ready to Repair'),
        ('2binvoiced', 'To be Invoiced'),
        ('invoice_except', 'Invoice Exception'),
        ('done', 'Repaired'),
        ('cancel', 'Cancelled')], string='Status',
        copy=False, default='draft', readonly=True, tracking=True,
        help="* The \'Draft\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Ready to Repair\' status is used to start to repairing, user can start repairing only after repair order is confirmed.\n"
             "* The \'To be Invoiced\' status is used to generate the invoice before or after repairing done.\n"
             "* The \'Done\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order.")
    location_id = fields.Many2one(
        'stock.location', 'Location',
        index=True, readonly=True, required=True, check_company=True,
        help="This is the location where the product to repair is located.",
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]})
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id','=', product_id), ('company_id', '=', company_id)]", check_company=True,
        help="Products repaired are all belonging to this lot")
    guarantee_limit = fields.Date('Warranty Expiration', states={'confirmed': [('readonly', True)]})
    # operations = fields.One2many(
    #     'repair.line', 'repair_id', 'Parts',
    #     copy=True, readonly=True, states={'draft': [('readonly', False)]})
    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist',
        default=lambda self: self.env['product.pricelist'].search([('company_id', 'in', [self.env.company.id, False])], limit=1).id,
        help='Pricelist of the selected partner.', check_company=True)
    currency_id = fields.Many2one(related='pricelist_id.currency_id')
    partner_invoice_id = fields.Many2one('res.partner', 'Invoicing Address', check_company=True)
    invoice_method = fields.Selection([
        ("none", "No Invoice"),
        ("b4repair", "Before Repair"),
        ("after_repair", "After Repair")], string="Invoice Method",
        default='none', index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')
    invoice_id = fields.Many2one(
        'account.move', 'Invoice',
        copy=False, readonly=True, tracking=True,
        domain=[('move_type', '=', 'out_invoice')])
    move_id = fields.Many2one(
        'stock.move', 'Move',
        copy=False, readonly=True, tracking=True, check_company=True,
        help="Move created by the repair order")
    # fees_lines = fields.One2many(
    #     'repair.fee', 'repair_id', 'Operations',
    #     copy=True, readonly=True, states={'draft': [('readonly', False)]})
    internal_notes = fields.Text('Internal Notes')
    quotation_notes = fields.Text('Quotation Notes')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user, check_company=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        readonly=True, required=True, index=True,
        default=lambda self: self.env.company)
    tag_ids = fields.Many2many('rma.tags', string="Tags")
    invoiced = fields.Boolean('Invoiced', copy=False, readonly=True)
    repaired = fields.Boolean('Repaired', copy=False, readonly=True)
    # amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    # amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    # amount_total = fields.Float('Total', compute='_amount_total', store=True)
    tracking = fields.Selection(string='Product Tracking', related="product_id.tracking", readonly=False)
    invoice_state = fields.Selection(string='Invoice State', related='invoice_id.state')

    @api.depends('partner_id')
    def _compute_default_address_id(self):
        for order in self:
            if order.partner_id:
                order.default_address_id = order.partner_id.address_get(['contact'])['contact']

    # @api.depends('operations.price_subtotal', 'invoice_method', 'fees_lines.price_subtotal', 'pricelist_id.currency_id')
    # def _amount_untaxed(self):
    #     for order in self:
    #         total = sum(operation.price_subtotal for operation in order.operations)
    #         total += sum(fee.price_subtotal for fee in order.fees_lines)
    #         order.amount_untaxed = order.pricelist_id.currency_id.round(total)

    # @api.depends('operations.price_unit', 'operations.product_uom_qty', 'operations.product_id',
    #              'fees_lines.price_unit', 'fees_lines.product_uom_qty', 'fees_lines.product_id',
    #              'pricelist_id.currency_id', 'partner_id')
    # def _amount_tax(self):
    #     for order in self:
    #         val = 0.0
    #         for operation in order.operations:
    #             if operation.tax_id:
    #                 tax_calculate = operation.tax_id.compute_all(operation.price_unit, order.pricelist_id.currency_id, operation.product_uom_qty, operation.product_id, order.partner_id)
    #                 for c in tax_calculate['taxes']:
    #                     val += c['amount']
    #         for fee in order.fees_lines:
    #             if fee.tax_id:
    #                 tax_calculate = fee.tax_id.compute_all(fee.price_unit, order.pricelist_id.currency_id, fee.product_uom_qty, fee.product_id, order.partner_id)
    #                 for c in tax_calculate['taxes']:
    #                     val += c['amount']
    #         order.amount_tax = val

    # @api.depends('amount_untaxed', 'amount_tax')
    # def _amount_total(self):
    #     for order in self:
    #         order.amount_total = order.pricelist_id.currency_id.round(order.amount_untaxed + order.amount_tax)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.guarantee_limit = False
        if (self.product_id and self.lot_id and self.lot_id.product_id != self.product_id) or not self.product_id:
            self.lot_id = False
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id

    @api.onchange('product_uom')
    def onchange_product_uom(self):
        res = {}
        if not self.product_id or not self.product_uom:
            return res
        if self.product_uom.category_id != self.product_id.uom_id.category_id:
            res['warning'] = {'title': _('Warning'), 'message': _('The product unit of measure you chose has a different category than the product unit of measure.')}
            self.product_uom = self.product_id.uom_id.id
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self = self.with_company(self.company_id)
        if not self.partner_id:
            self.address_id = False
            self.partner_invoice_id = False
            self.pricelist_id = self.env['product.pricelist'].search([
                ('company_id', 'in', [self.env.company.id, False]),
            ], limit=1)
        else:
            addresses = self.partner_id.address_get(['delivery', 'invoice', 'contact'])
            self.address_id = addresses['delivery'] or addresses['contact']
            self.partner_invoice_id = addresses['invoice']
            self.pricelist_id = self.partner_id.property_product_pricelist.id

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
            self.location_id = warehouse.lot_stock_id
        else:
            self.location_id = False

    def unlink(self):
        for order in self:
            if order.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a repair order once it has been confirmed. You must first cancel it.'))
            if order.state == 'cancel' and order.invoice_id and order.invoice_id.posted_before:
                raise UserError(_('You can not delete a repair order which is linked to an invoice which has been posted once.'))
        return super().unlink()

    @api.model
    def create(self, vals):
        # To avoid consuming a sequence number when clicking on 'Create', we preprend it if the
        # the name starts with '/'.
        vals['name'] = vals.get('name') or '/'
        if vals['name'].startswith('/'):
            vals['name'] = (self.env['ir.sequence'].next_by_code('rma.rma') or '/') + vals['name']
            vals['name'] = vals['name'][:-1] if vals['name'].endswith('/') and vals['name'] != '/' else vals['name']
        return super(RMA, self).create(vals)

    def action_validate(self):
        self.ensure_one()
        # if self.filtered(lambda repair: any(op.product_uom_qty < 0 for op in repair.operations)):
        #     raise UserError(_("You can not enter negative quantities."))
        if self.product_id.type == 'consu':
            return self.action_repair_confirm()
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        available_qty_owner = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id, self.lot_id, owner_id=self.partner_id, strict=True)
        available_qty_noown = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id, self.lot_id, strict=True)
        repair_qty = self.product_uom._compute_quantity(self.product_qty, self.product_id.uom_id)
        for available_qty in [available_qty_owner, available_qty_noown]:
            if float_compare(available_qty, repair_qty, precision_digits=precision) >= 0:
                return self.action_repair_confirm()
        else:
            return {
                'name': self.product_id.display_name + _(': Insufficient Quantity To Repair'),
                'view_mode': 'form',
                'res_model': 'stock.warn.insufficient.qty.repair',
                'view_id': self.env.ref('repair.stock_warn_insufficient_qty_repair_form_view').id,
                'type': 'ir.actions.act_window',
                'context': {
                    'default_product_id': self.product_id.id,
                    'default_location_id': self.location_id.id,
                    'default_repair_id': self.id,
                    'default_quantity': repair_qty,
                    'default_product_uom_name': self.product_id.uom_name
                },
                'target': 'new'
            }

    def action_repair_confirm(self):
        """ Repair order state is set to 'To be invoiced' when invoice method
        is 'Before repair' else state becomes 'Confirmed'.
        @param *arg: Arguments
        @return: True
        """
        if self.filtered(lambda repair: repair.state != 'draft'):
            raise UserError(_("Only draft repairs can be confirmed."))
        self._check_company()
        # self.operations._check_company()
        # self.fees_lines._check_company()
        before_repair = self.filtered(lambda repair: repair.invoice_method == 'b4repair')
        before_repair.write({'state': '2binvoiced'})
        to_confirm = self - before_repair
        # to_confirm_operations = to_confirm.mapped('operations')
        # to_confirm_operations.write({'state': 'confirmed'})
        to_confirm.write({'state': 'confirmed'})
        # Create MO to do the repair work
        for rep in to_confirm:
            rep.production_id = self.env['mrp.production'].create({
                'product_id':rep.product_id.id,
                'product_qty':rep.product_qty,
                'product_uom_id':rep.product_uom.id,
                'rma_id':rep.id,
            })
        return True



class RMATags(models.Model):
    """ Tags of Repair's tasks """
    _name = "rma.tags"
    _description = "RMA Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]


# stock.return.picking
# def create_returns()