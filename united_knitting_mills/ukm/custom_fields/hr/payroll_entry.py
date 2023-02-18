import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def payroll_entry_customizations():
    payroll_entry_property_setter()
    payroll_entry_custom_fields()

def payroll_entry_custom_fields():
    custom_fields = {
		"Payroll Entry": [
			dict(fieldname='location', label='Location',
				fieldtype='Link', options='Location',insert_after='accounting_dimensions_section', reqd=1),
            dict(fieldname='ts_column_break',
				fieldtype='Column Break',insert_after='start_date'),
        ]
    }
    create_custom_fields(custom_fields)

def payroll_entry_property_setter():
    make_property_setter("Payroll Entry", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Payroll Entry", "company", "hidden", 1, "Check")
    make_property_setter("Payroll Entry", "currency", "default", "INR", "Text")
    make_property_setter("Payroll Entry", "account", "hidden", 1, "Section Break")
    make_property_setter("Payroll Entry", "section_break_13", "hidden", 1, "Section Break")
    make_property_setter("Payroll Entry", "currency", "hidden", 1, "Check")
    make_property_setter('Payroll Entry', 'payroll_frequency', 'default', 'Monthly', 'Select')
    make_property_setter('Payroll Entry', 'payroll_frequency', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'branch', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'validate_attendance', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'section_break_12', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'deduct_tax_for_unclaimed_employee_benefits', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'deduct_tax_for_unsubmitted_tax_exemption_proof', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'project', 'hidden', 1, 'Select')
    make_property_setter('Payroll Entry', 'cost_center', 'hidden', 1, 'Select')
