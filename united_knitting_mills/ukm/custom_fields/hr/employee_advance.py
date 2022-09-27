from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def employee_advance_customisation():
    employee_advance_custom_fields()
    employee_advance_property_setter()

def employee_advance_custom_fields():
    custom_fields = {
		"Employee Advance": [
            dict(fieldname='location', label='Location',
				fieldtype='Link',options='Location',insert_after='mode_of_payment',
                fetch_from='employee.location')
            ]
    }
    create_custom_fields(custom_fields)
def employee_advance_property_setter():
    pass