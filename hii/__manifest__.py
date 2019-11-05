# Copyright 2019 Kitti U. <kittiu@ecosoft.co.th>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Type",
    "version": "12.0.1.0.0",
    "category": "Hydro Informatics Institute",
    "author": "Ecosoft,Odoo Community Association (OCA)",
    "website": "https://github.com/ecosoft-odoo/hii",
    "license": "AGPL-3",
    "depends": [
        'purchase_stock',
        'account',
        'budget_control',
        'budget_control_expense',
        'budget_control_purchase',
        # 'budget_control_purchase_request',
        'analytic_tag_dimension_enhanced',
        'budget_control_tag_dimension',
        'budget_control_expense_tag_dimension',
        'budget_control_purchase_tag_dimension',
        'budget_control_tier_validation',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/dimension_security.xml',
        'views/dimension_view.xml',
    ],
    'installable': True,
}
