import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def holiday_list_customisation():
    holiday_list_custom_fields()
    holiday_list_property_setter()

def holiday_list_custom_fields():
    pass

def holiday_list_property_setter():
    make_property_setter("Holiday List", "color", "hidden", 1, "Check")
    make_property_setter("Holiday List", "holidays_section", "collapsible", 1, "Section Break")