from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_salary_structure_fields():
	custom_fields = {
		"Salary Structure": [
			dict(fieldname='salary_component_', label='Salary Component',
				fieldtype='Link', options='Salary Component' ,insert_after='hour_rate', reqd=1)]
	}
	create_custom_fields(custom_fields)
	create_salary_structure_property_setter()

def create_salary_structure_property_setter():
	make_property_setter('Salary Structure', 'earnings', 'hidden', 1, 'Check')