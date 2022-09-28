import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_structure_assignment_customizations():
    create_property_setter()
    create_customm_fields()

def create_customm_fields():
    custom_fields = {
		"Salary Structure Assignment": [
			dict(fieldname='unit', label='Unit',reqd=1,
				fieldtype='Link',options='Location',insert_after='department',fetch_from='employee.location'),
            dict(fieldname='min_wages', label='Minimum Wages',
				fieldtype='Currency',insert_after='designation_name',fetch_from='designation.min_wages')  , 
			]
	}
    create_custom_fields(custom_fields)

def create_property_setter():
    make_property_setter("Salary Structure Assignment", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Salary Structure Assignment", "salary_structure", "default", "Default Structure", "Link")
    make_property_setter("Salary Structure Assignment", "company", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "currency", "default", "INR", "Text")
    make_property_setter("Salary Structure Assignment", "currency", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "variable", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "payroll_payable_account", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "income_tax_slab", "hidden", 1, "Check")