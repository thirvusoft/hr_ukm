from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_salary_structure_fields():
    custom_fields = {
		"Salary Structure": [
			dict(fieldname='salary_slip_based_on_shift', label='Salary Slip Based On shift',
				fieldtype='Check', insert_after='salary_slip_based_on_timesheet'),
			dict(fieldname='salary_component_', label='Salary Component',
				fieldtype='Link', depends_on='eval:doc.salary_slip_based_on_shift==1',options='Salary Component',mandatory_depends_on='eval:doc.salary_slip_based_on_shift==1',insert_after='hour_rate'),        ]
    }
    create_custom_fields(custom_fields)