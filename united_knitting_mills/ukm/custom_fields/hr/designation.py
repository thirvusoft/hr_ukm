import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def designation_customisation():
    create_designation_custom_fields()
    designation_property_setter()
    
def create_designation_custom_fields():
    custom_fields = {
		"Designation": [
            dict(fieldname='min_wages', label='Minimum Wages',
				fieldtype='Currency',insert_after='designation_name',reqd =1)  ,     
            dict(fieldname='ts_column_break',
				fieldtype='Column Break',insert_after='min_wages'),
			dict(fieldname='thirvu_shift', label='Thirvu Shift',
				fieldtype='Link',options='Employee Timing Details',insert_after='ts_column_break',reqd =1)
            ]
    }
    create_custom_fields(custom_fields)

def designation_property_setter():
    make_property_setter("Designation", "description", "hidden", 1, "Check")
    make_property_setter("Designation", "required_skills_section", "hidden", 1, "Section Break")