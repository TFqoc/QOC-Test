# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'
    
    @api.depends('qty_done', 'component_remaining_qty')
    def _compute_component_qty_to_do(self):
        for wo in self:
            wo.component_qty_to_do = 12
        raise Warning("Overwrite successful.")
