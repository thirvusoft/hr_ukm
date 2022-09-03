from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_payroll_entry_fields():
    custom_fields = {
		"Payroll Entry": [
			dict(fieldname='location', label='Location',
				fieldtype='Link', options='Location',insert_after='accounting_dimensions_section', hidden=1),
        ]
    }
    create_custom_fields(custom_fields)