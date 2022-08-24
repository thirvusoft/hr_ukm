import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def designation_customisation():
    create_designation_custom_fields()
   
def create_designation_custom_fields():
    custom_fields = {
		"Designation": [
			dict(fieldname='thirvu_shift', label='Thirvu Shift',
				fieldtype='Link',options='Employee Timing Details',insert_after='designation_name',reqd =1)
            ]
    }
    create_custom_fields(custom_fields)