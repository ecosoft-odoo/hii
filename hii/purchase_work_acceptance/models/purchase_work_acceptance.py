# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WorkAcceptance(models.Model):
    _inherit = "work.acceptance"

    responsible_id = fields.Many2one(
        required=False,
    )
    committee_ids = fields.One2many(
        comodel_name='work.acceptance.committee',
        inverse_name='wa_id',
        string='Committee Lines',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )


class WorkAcceptanceCommittee(models.Model):
    _name = 'work.acceptance.committee'
    _description = 'Work Acceptance Committee'

    wa_id = fields.Many2one(
        comodel_name='work.acceptance',
        string='WA Reference',
        index=True,
        required=True,
        ondelete='cascade'
    )
    committee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible Person',
        required=True,
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job',
        readonly=True,
    )
    description = fields.Char(
        string='Description',
    )

    @api.onchange('committee_id')
    def _onchange_job_id(self):
        if self.committee_id:
            self.job_id = self.committee_id.job_id
