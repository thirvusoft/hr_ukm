from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_salary_slip_fields():
    custom_fields = {
		"Salary Slip": [
			dict(fieldname='total_shift_worked', label='Total Shift Worked',
				fieldtype='Data', insert_after='total_working_days',read_only=1),
        ]
    }
    create_custom_fields(custom_fields)