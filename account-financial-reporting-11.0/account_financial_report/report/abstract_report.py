# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AbstractReport(models.AbstractModel):
    _name = 'account_financial_report_abstract'

    def _transient_clean_rows_older_than(self, seconds):
        assert (
            self._transient
        ), f"Model {self._name} is not transient, it cannot be vacuumed!"
        # Never delete rows used in last 5 minutes
        seconds = max(seconds, 300)
        query = """
DELETE FROM """ + self._table + """
WHERE COALESCE(
    write_date, create_date, (now() at time zone 'UTC'))::timestamp
    < ((now() at time zone 'UTC') - interval %s)
"""
        self.env.cr.execute(query, (f"{seconds} seconds", ))
