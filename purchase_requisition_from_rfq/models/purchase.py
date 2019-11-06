# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def write(self, vals):
        for rec in self:
            super(PurchaseOrder, rec).write(vals)

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        PR = self.env['purchase.requisition']
        PRLine = self.env['purchase.requisition.line']
        for order in self:
            if order.requisition_id:
                order.auto_cancel_another_order()
                agreement = PR.browse(order.requisition_id.id)
                agreement['vendor_id'] = order.partner_id.id
                pr_lines = PRLine.search(
                    [('requisition_id', '=', order.requisition_id.id)])
                for line in pr_lines:
                    price_unit = order.order_line.filtered(
                        lambda l: l.product_id == line.product_id)\
                        .mapped('price_unit')
                    if price_unit:
                        line['price_unit'] = price_unit[0]
        return res

    def auto_cancel_another_order(self):
        requisition_id = self.requisition_id.id
        purchases = self.env['purchase.order'].search(
            [('requisition_id', '=', requisition_id)])
        for purchase in purchases:
            if purchase.state != 'purchase':
                purchase.state = 'cancel'
