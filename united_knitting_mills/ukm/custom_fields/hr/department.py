import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def department_customisation():
    create_department_custom_fields()
    department_property_setter()

def create_department_custom_fields():
    custom_fields = {
		"Department": [
			dict(fieldname='department_approvers', label='Department Approvers',
				fieldtype='Table',options='Department Approvers',insert_after='approvers'),
            dict(fieldname='unit', label='Unit',reqd=1,
				fieldtype='Link',options='Location',insert_after='company'),
            dict(fieldname='is_staff', label='Is Staff',
				fieldtype='Check',insert_after='unit')
            ]
    }
    create_custom_fields(custom_fields)

def department_property_setter():
    make_property_setter("Department", "section_break_4", "hidden", 1, "Section Break")
    make_property_setter("Department", "is_group", "hidden", 1, "Check")
    make_property_setter("Department", "department_approvers", "hidden", 1, "Check")
    make_property_setter("Department", "expense_approvers", "hidden", 1, "Check")
    make_property_setter("Department", "shift_request_approver", "hidden", 1, "Check")
    make_property_setter("Department", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Department", "company", "hidden", 1, "Check")