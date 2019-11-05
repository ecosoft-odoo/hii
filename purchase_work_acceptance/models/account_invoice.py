# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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
        help='To control quantity and unit price of the vendor bill, to be '
             'according to the quantity and unit price of the work acceptance.',
    )

    def _get_require_wa(self):
        return self.env.user.has_group(
            'purchase_work_acceptance.group_work_acceptance_enforce')

    def _prepare_invoice_line_from_po_line(self, line):
        res = super()._prepare_invoice_line_from_po_line(line)
        wa_line = self.wa_id.wa_line_ids.filtered(
            lambda l: l.purchase_line_id == line)
        if wa_line:
            res['quantity'] = wa_line['product_qty']
            res['uom_id'] = wa_line['product_uom']
        return res

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        for rec in self:
            if rec.wa_id:
                rec.currency_id = rec.wa_id.currency_id
        return super().purchase_order_change()

    @api.multi
    def action_invoice_open(self):
        # WALine = self.env['work.acceptance.line']
        # for rec in self:
        #     if rec.wa_id:
        #         inv_dict = {}
        #         for order in orders:
        #             # Test combination of product and quantity
        #             po_dict[order.id] = [(line.product_id.id, line.product_qty)
        #                                  for line in order.order_line]
        #
        #         test_po = po_dict.pop(id_max)
        #         for test_line in test_po:
        #             for key in po_dict.keys():
        #                 if (po_dict[key].count(test_line) != test_po.count(test_line)):
        #                     raise ValidationError(_('The purchase agreement cannot be '
        #                                             'processed because the order '
        #                                             'are different!'))
                # for line in rec.invoice_line_ids:
                #     po_line_id = line.purchase_line_id.id
                #     wa_lines = WALine.search([
                #         ('purchase_line_id', '=', po_line_id),
                #         ('wa_id', '=', rec.wa_id.id)], limit=1)
                #     if line.quantity != wa_lines.product_qty or \
                #             line.price_unit != wa_lines.price_unit:
                #         raise ValidationError(_('You cannot validate a bill if'
                #                                 ' Quantity more than accepted'
                #                                 ' quantity'))
        return super().action_invoice_open()
