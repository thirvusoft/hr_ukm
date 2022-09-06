import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def holiday_list_customisation():
    holiday_list_custom_fields()
    holiday_list_property_setter()

def holiday_list_custom_fields():
    custom_fields = {
		"Holiday List": [
            dict(fieldname='unit', label='Unit',reqd=1,
				fieldtype='Link',options='Location',insert_after='total_holidays')
            ]
    }
    create_custom_fields(custom_fields)


def holiday_list_property_setter():
    make_property_setter("Holiday List", "color", "hidden", 1, "Check")
    make_property_setter("Holiday List", "holidays_section", "collapsible", 1, "Section Break")