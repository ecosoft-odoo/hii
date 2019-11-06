# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.name:
            super().onchange_product_id()
        else:
            self.keep_description = True
            if self.product_qty < 1.0:
                self.product_qty = 1.0
