from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
		"Account": [
			dict(fieldname='location', label='Location',
                fieldtype='Link',options='Location', insert_after='balance_must_be', read_only=0,reqd=1)
			
            ]
    }
    create_custom_fields(custom_fields)