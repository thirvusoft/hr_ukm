import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_structure_customizations():
	salary_structure_property_setter()
	salary_structure_custom_fields()

def salary_structure_custom_fields():
	custom_fields = {
		"Salary Structure": [
			dict(fieldname='salary_component_', label='Salary Component',
				fieldtype='Link', options='Salary Component' ,insert_after='hour_rate', reqd=1),
			dict(fieldname='unit', label='Unit',reqd=1,
				fieldtype='Link',options='Location',insert_after='company')
			]
	}
	create_custom_fields(custom_fields)

def salary_structure_property_setter():
	make_property_setter('Salary Structure', 'earnings', 'hidden', 1, 'Check')
	make_property_setter("Salary Structure", "letter_head", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "company", "default", "United Knitting Mills", "Text")
	make_property_setter("Salary Structure", "company", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "is_active", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "currency", "default", "INR", "Text")
	make_property_setter("Salary Structure", "currency", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "payroll_frequency", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "salary_slip_based_on_timesheet", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "leave_encashment_amount_per_day", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "max_benefits", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "account", "hidden", 1, "Check")
	make_property_setter("Salary Structure", "deductions", "hidden", 1, "Section Break")
	make_property_setter("Salary Structure", "conditions_and_formula_variable_and_example", "hidden", 1, "Check")