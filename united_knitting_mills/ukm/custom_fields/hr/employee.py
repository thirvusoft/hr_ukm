from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_employee_fields():
    custom_fields = {
		"Employee": [
			dict(fieldname='location', label='Location',
				fieldtype='Link',options='Location', insert_after='last_name', read_only=0),
			dict(fieldname='abbr', label='Abbreviation',
				fieldtype='Data', insert_after='location', hidden=1,fetch_from='location.abbr'),
            dict(fieldname='enable_esi', label='Enable ESI',
				fieldtype='Check', insert_after='date_of_joining', hidden=1),
            dict(fieldname='enable_pf', label='Enable PF',
				fieldtype='Check', insert_after='enable_esi', hidden=1),
        ]
    }
    create_custom_fields(custom_fields)