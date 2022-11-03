import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def leave_type_customizations():
    leave_type_property_setter()
    leave_type_custom_fields()
    
def leave_type_property_setter():
    make_property_setter("Leave Type", "carry_forward_section", "hidden", 1, "Check")
    make_property_setter("Leave Type", "encashment", "hidden", 1, "Check")
    make_property_setter("Leave Type", "earned_leave", "hidden", 1, "Check")
    
def leave_type_custom_fields():
    custom_field = {
        'Leave Type':[
            dict(
                fieldname='is_pay_leave', label='Is Pay Leave', fieldtype='Check', insert_after='leave_type_name', 
            ),
            dict(fieldname='ts_section_break', label='', fieldtype='Section Break', insert_after='is_pay_leave',hidden=1)
        ]
    }
    create_custom_fields(custom_field)