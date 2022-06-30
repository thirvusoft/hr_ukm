from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_salary_slip_fields():
    custom_fields = {
		"Salary Slip": [
			dict(fieldname='salary_slip_based_on_shift', label='Salary Slip Based On shift',
				fieldtype='Check', insert_after='salary_slip_based_on_timesheet'),
			dict(fieldname='total_shift_worked', label='Total Shift Worked',
				fieldtype='Data', insert_after='total_working_days',depends_on='eval:doc.salary_slip_based_on_shift==1',read_only=1),
        ]
    }
    create_custom_fields(custom_fields)