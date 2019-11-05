# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Picking(models.Model):
    _inherit = "stock.picking"

    require_wa = fields.Boolean(
        default=lambda self: self._get_require_wa(),
    )
    wa_id = fields.Many2one(
        comodel_name='work.acceptance',
        string='WA Reference',
        copy=False,
        domain=lambda self: [
            ('state', '=', 'accept'),
            ('purchase_id', '=', self._context.get('active_id'))],
    )

    def _get_require_wa(self):
        return self.env.user.has_group(
            'purchase_work_acceptance.group_work_acceptance_enforce')

    @api.multi
    def button_validate(self):
        if self.wa_id:
            WALines = self.env['work.acceptance.line']
            wa_products = WALines.search([('wa_id', '=', self.wa_id.id)])\
                .mapped('product_id')\
                .filtered(lambda product: product.type != 'service')
            Moves = self.env['stock.move']
            move_products = Moves.search(
                [('picking_id', '=', self.id)]).mapped('product_id')
            if len(move_products) != len(wa_products):
                raise ValidationError(_('You cannot validate a transfer if done'
                                      ' quantity not equal accepted quantity'))
            for product in move_products:
                wa_product = WALines.search([
                    ('wa_id', '=', self.wa_id.id), ('product_id', '=', product.id)])
                move_product = Moves.search([
                    ('picking_id', '=', self.id), ('product_id', '=', product.id)])
                if sum(wa_product.mapped('product_qty')) != \
                        sum(move_product.mapped('quantity_done')):
                    raise ValidationError(_('You cannot validate a transfer if done'
                                          ' quantity not equal accepted quantity'))
        return super(Picking, self).button_validate()

    @api.onchange('wa_id')
    def _onchange_wa_id(self):
        if self.wa_id:
            for move in self.move_ids_without_package:
                move.quantity_done = move.product_uom_qty
