# Copyright 2015-2019 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""
Strategy -> CostCenter
ProfitCenter
"""

from odoo import fields, models


class Strategy(models.Model):
    _name = 'strategy'
    _description = 'Strategy'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id
    )

class CostCenter(models.Model):
    _name = 'costcenter'
    _description = 'Cost Center'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id
    )
    strategy_id = fields.Many2one(
        comodel_name='strategy',
        required=True,
    )


class ProfitCenter(models.Model):
    _name = 'profitcenter'
    _description = 'Profit Center'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id
    )
