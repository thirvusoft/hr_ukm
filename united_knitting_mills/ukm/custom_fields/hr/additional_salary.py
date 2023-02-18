import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def additional_salary_customizations():
    additional_salary_property_setter()
    additional_salary_custom_fields()

def additional_salary_property_setter():
    make_property_setter("Additional Salary", "overwrite_salary_structure_amount", "default", "0", "Text")


def additional_salary_custom_fields():
    pass