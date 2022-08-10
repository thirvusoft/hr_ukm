from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_location_fields():
    custom_fields = {
		"Location": [
			dict(fieldname='abbr', label='Abbreviation',
				fieldtype='Data', insert_after='area'),
        dict(fieldname='sec_break', label='',
				fieldtype='Section Break', insert_after='abbr'),
        dict(fieldname='user_list', label='User List',
				fieldtype='Table',options='Thirvu Location User', insert_after='sec_break')],
    }
    create_custom_fields(custom_fields)