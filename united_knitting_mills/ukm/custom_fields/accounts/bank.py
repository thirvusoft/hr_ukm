import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def bank_customization():
    new_fields()
    property_setter()

def new_fields():
    pass


def property_setter():
    make_property_setter("Bank", "swift_number", "allow_in_quick_entry", 0, "Check")