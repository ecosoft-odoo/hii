# Copyright 2019 Apps2GROW - Henrik Norlin
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2 import sql
from odoo.tools import float_is_zero


def adjust_asset_values(env):
    """Avoid method_time != 'year' when possible + adjust other values
    in assets and asset profiles.
    """
    # Copy analytic account value
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_asset aa
        SET account_analytic_id = aap.account_analytic_id
        FROm account_asset_profile aap
        WHERE aa.profile_id = aap.id""",
    )
    # Adjust method_time, method_number and method_period
    number = sql.Identifier(openupgrade.get_legacy_name('method_number'))
    period = sql.Identifier(openupgrade.get_legacy_name('method_period'))
    for table in ['account_asset_profile', 'account_asset']:
        table = sql.Identifier(table)
        openupgrade.logged_query(
            env.cr, sql.SQL("""
            UPDATE {table}
            SET method_time = 'year',
                method_number = ({number} * {period}) / 12
            WHERE MOD({number} * {period}, 12) = 0
            """).format(
                number=number,
                period=period,
                table=table,
            ),
        )
        openupgrade.logged_query(
            env.cr, sql.SQL("""
            UPDATE {table}
            SET method_period = (CASE
                    WHEN {period} = 1 THEN 'month'
                    WHEN {period} = 3 THEN 'quarter'
                    WHEN {period} = 12 THEN 'year'
                END)
            WHERE {period} IN (1, 3, 12)
            """).format(
                period=period,
                table=table,
            ),
        )


def adjust_aml_values(env):
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_move_line aml
        SET asset_id = aa.id,
            asset_profile_id = aa.profile_id
        FROM account_asset aa,
            account_asset_line aal
        WHERE aal.move_id = aml.move_id
            AND aa.id = aal.asset_id""",
    )


def handle_account_asset_disposal_migration(env):
    """Take care of potentially installed `account_asset_disposal` module.

    In this phase we set the last asset line to the type remove on the
    corresponding assets.
    """
    column_name = openupgrade.get_legacy_name('disposal_move_id')
    if not openupgrade.column_exists(env.cr, 'account_asset', column_name):
        return
    env.cr.execute(
        sql.SQL(
            "SELECT id FROM account_asset WHERE {col} IS NOT NULL"
        ).format(col=sql.Identifier(column_name))
    )
    assets = env['account.asset'].with_context(
        allow_asset_line_update=True,
    ).browse(x[0] for x in env.cr.fetchall())
    assets.mapped('depreciation_line_ids').filtered(
        lambda x: float_is_zero(
            x.remaining_value,
            precision_rounding=x.asset_id.company_currency_id.rounding,
        )
    ).write({'type': 'remove'})


@openupgrade.migrate()
def migrate(env, version):
    copied_column = openupgrade.get_legacy_name('method_time')
    if not openupgrade.column_exists(env.cr, 'account_asset', copied_column):
        # We avoid this migration if `account_asset` was not installed in v11
        return
    adjust_asset_values(env)
    adjust_aml_values(env)
    handle_account_asset_disposal_migration(env)
