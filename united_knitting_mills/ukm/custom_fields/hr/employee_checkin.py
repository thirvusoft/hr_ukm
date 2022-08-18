import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def checkin_customisation():
    checkin_property_setter()
    create_checkin_custom_fields()
   
def checkin_property_setter():
    pass


def create_checkin_custom_fields():
    custom_fields = {
		"Employee Checkin": [
			dict(fieldname='designation', label='Designation',
				fieldtype='Link',options='Designation',insert_after='employee_name',read_only=1,fetch_from='employee.designation'),
            ]
    }
    create_custom_fields(custom_fields)