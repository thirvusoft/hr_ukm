from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def create_payroll_entry_fields():
		custom_fields = {
		"Payroll Entry": [
			dict(fieldname='location', label='Location',
				fieldtype='Link', options='Location',insert_after='accounting_dimensions_section', hidden=1),
				]
		}
		create_custom_fields(custom_fields)
		create_payroll_entry_property_setter()

def create_payroll_entry_property_setter():
		make_property_setter('Payroll Entry', 'payroll_frequency', 'default', 'Monthly', 'Select')
		make_property_setter('Payroll Entry', 'payroll_frequency', 'hidden', 1, 'Select')

	