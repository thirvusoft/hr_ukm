import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def department_customisation():
    create_department_custom_fields()
   
def create_department_custom_fields():
    custom_fields = {
		"Department": [
			dict(fieldname='department_approvers', label='Department Approvers',
				fieldtype='Table',options='Department Approvers',insert_after='approvers')
            ]
    }
    create_custom_fields(custom_fields)