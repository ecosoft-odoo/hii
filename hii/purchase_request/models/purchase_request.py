# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    request_employee_id = fields.Many2one(
        comodel_name='hr.employee',
        compute='_compute_request_employee_id'
    )
    assigned_to = fields.Many2one(
        compute='_compute_assigned_to',
    )

    @api.multi
    def _compute_request_employee_id(self):
        request_employee_id = self.env['hr.employee'].search(
            [('user_id', '=', self.requested_by.id)], limit=1)
        self.request_employee_id = request_employee_id.id

    @api.multi
    def _compute_assigned_to(self):
        review_ids = self.review_ids.filtered(lambda r: r.status != 'approved')
        if not review_ids and self.review_ids:
            self.assigned_to = self.env.user

    @api.multi
    def validate_tier(self):
        res = super().validate_tier()
        if self.assigned_to:
            self.button_approved()
        return res
