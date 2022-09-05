import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_structure_assignment_customizations():
    create_property_setter()
    create_custom_fields()

def create_custom_fields():
    pass

def create_property_setter():
    make_property_setter("Salary Structure Assignment", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Salary Structure Assignment", "company", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "variable", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "payroll_payable_account", "hidden", 1, "Check")