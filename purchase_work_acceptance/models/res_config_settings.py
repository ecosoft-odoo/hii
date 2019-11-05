# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_work_acceptance = fields.Boolean(
        string="Enable work acceptance process",
        implied_group='purchase_work_acceptance.group_work_acceptance',
    )
    group_work_acceptance_enforce = fields.Boolean(
        string="Enforce work acceptance on every purchase",
        implied_group='purchase_work_acceptance.group_work_acceptance_enforce',
    )
