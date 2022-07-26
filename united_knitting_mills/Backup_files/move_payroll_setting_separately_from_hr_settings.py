# Copyright (c) 2019, Frappe and Contributors
# License: GNU General Public License v3. See license.txt


import frappe


def execute(): #quarter day in Line 19 , Three Quarter Day in line 20
	data = frappe.db.sql(
		"""SELECT *
        FROM `tabSingles`
        WHERE
            doctype = "HR Settings"
        AND
            field in (
                "encrypt_salary_slips_in_emails",
                "email_salary_slip_to_employee",
                "daily_wages_fraction_for_half_day",
                "fraction_of_daily_salary_for_quarter_day",
                "fraction_of_daily_salary_for_three_quarter_day",
                "fraction_of_daily_salary_for_one_quarter_day",
                "fraction_of_daily_salary_for_one_half_day",
                "disable_rounded_total",
                "include_holidays_in_total_working_days",
                "max_working_hours_against_timesheet",
                "payroll_based_on",
                "password_policy"
            )
            """,
		as_dict=1,
	)

	for d in data:
		frappe.db.set_value("Payroll Settings", None, d.field, d.value)
