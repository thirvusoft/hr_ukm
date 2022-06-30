from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_company_fields():
    custom_fields = {
		"Location": [
			dict(fieldname='abbr', label='Abbreviation',
				fieldtype='Data', insert_after='area'),
			
            ]
    }
    create_custom_fields(custom_fields)