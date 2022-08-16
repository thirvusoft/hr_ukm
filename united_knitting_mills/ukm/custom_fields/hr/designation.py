import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def designation_customisation():
    create_designation_custom_fields()
   
def create_designation_custom_fields():
    custom_fields = {
		"Designation": [
			dict(fieldname='thirvu_shift', label='Thirvu Shift',
				fieldtype='Link',options='Thirvu Shift',insert_after='description')
            ]
    }
    create_custom_fields(custom_fields)