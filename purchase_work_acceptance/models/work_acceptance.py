# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class WorkAcceptance(models.Model):
    _name = 'work.acceptance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Work Acceptance'
    _order = 'id desc'

    name = fields.Char(
        required=True,
        index=True,
        copy=False,
        default='New'
    )
    date_due = fields.Datetime(
        string='Due Date',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    date_receive = fields.Datetime(
        string='Received Date',
        default=fields.Datetime.now,
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    date_accept = fields.Datetime(
        string='Accepted Date',
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor',
        required=True,
        change_default=True,
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible Person',
        required=True,
        change_default=True,
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True,
        readonly=True,
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('accept', 'Accepted'),
         ('cancel', 'Cancelled')],
        string='Status',
        readonly=True,
        index=True,
        copy=False,
        default='draft',
        track_visibility='onchange'
    )
    wa_line_ids = fields.One2many(
        comodel_name='work.acceptance.line',
        inverse_name='wa_id',
        string='Work Acceptance Lines',
    )
    notes = fields.Text(
        string='Notes',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        related='wa_line_ids.product_id',
        string='Product',
        readonly=False,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Work Acceptance Representative',
        default=lambda self: self.env.user,
        index=True,
        track_visibility='onchange',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        required=True,
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    purchase_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase Order',
        readonly=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'work.acceptance') or '/'
        return super(WorkAcceptance, self).create(vals)

    @api.multi
    def button_accept(self, force=False):
        self.write({'state': 'accept', 'date_accept': fields.Datetime.now()})

    @api.multi
    def button_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def button_cancel(self):
        self.write({'state': 'cancel'})


class WorkAcceptanceLine(models.Model):
    _name = 'work.acceptance.line'
    _description = 'Work Acceptance Line'
    _order = 'id'

    name = fields.Text(
        string='Description',
        required=True
    )
    product_qty = fields.Float(
        string='Quantity',
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string='Product Unit of Measure',
        required=True,
    )
    price_unit = fields.Float(
        string='Unit Price',
        readonly=True,
    )
    price_subtotal = fields.Monetary(
        compute='_compute_amount',
        string='Subtotal',
    )
    wa_id = fields.Many2one(
        comodel_name='work.acceptance',
        string='WA Reference',
        index=True,
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='wa_id.partner_id',
        string='Partner',
        readonly=True,
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        related='wa_id.responsible_id',
        string='Responsible Person',
        readonly=True,
    )
    currency_id = fields.Many2one(
        related='wa_id.currency_id',
        string='Currency',
        readonly=True,
    )
    date_due = fields.Datetime(
        related='wa_id.date_due',
        string='Due Date',
        readonly=True,
    )
    date_receive = fields.Datetime(
        related='wa_id.date_receive',
        string='Received Date',
        readonly=True,
    )
    date_accept = fields.Datetime(
        related='wa_id.date_accept',
        string='Accepted Date',
        readonly=True,
    )
    purchase_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string='Purchase Order Line',
        ondelete='set null',
        index=True,
        readonly=True,
    )

    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit