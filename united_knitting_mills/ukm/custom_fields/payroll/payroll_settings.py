from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_payroll_settings_fields():
    custom_fields = {
		"Payroll Settings": [
			dict(fieldname='fraction_of_daily_salary_for_quarter_day', label='Fraction of Daily Salary for Quarter Day',
				fieldtype='Float', insert_after='salary_slip_based_on_timesheet',default='0.25'),
			dict(fieldname='fraction_of_daily_salary_for_three_quarter_day', label='Fraction of Daily Salary for Three Quarter Day',
				fieldtype='Float', insert_after='fraction_of_daily_salary_for_quarter_day',default='0.75'),
            dict(fieldname='fraction_of_daily_salary_for_one_half_day', label='Fraction of Daily Salary for One Half Day',
				fieldtype='Float', insert_after='fraction_of_daily_salary_for_three_quarter_day',default='1.50'),
            dict(fieldname='fraction_of_daily_salary_for_one_quarter_day', label='Fraction of Daily Salary for One Quarter Day',
				fieldtype='Float', insert_after='fraction_of_daily_salary_for_one_half_day',default='1.25')
        ]
    }
    create_custom_fields(custom_fields)