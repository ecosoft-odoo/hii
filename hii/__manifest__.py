# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "HII Customization",
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
        # 'analytic_tag_dimension_enhanced',
        'budget_control_tag_dimension',
        'budget_control_expense_tag_dimension',
        'budget_control_purchase_tag_dimension',
        'budget_control_tier_validation',
        'hr',
        'base_tier_validation_formula',
        'purchase_request_tier_validation',
        'purchase_work_acceptance',
    ],
    "data": [
        'budget_dimension/security/ir.model.access.csv',
        'budget_dimension/security/dimension_security.xml',
        'budget_dimension/views/dimension_view.xml',
        'hr/data/hr_data.xml',
        'purchase_request/data/purchase_request_tier_definition.xml',
        'purchase_request/views/purchase_request_view.xml',
        'purchase_work_acceptance/security/ir.model.access.csv',
        'purchase_work_acceptance/views/work_acceptance_views.xml',
    ],
    'installable': True,
}
