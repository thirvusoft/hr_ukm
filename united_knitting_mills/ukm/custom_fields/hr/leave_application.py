import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def leave_application_customizations():
    create_property_setter()
    create_custom_fields_()
    
def create_property_setter():
    make_property_setter('Leave Application', "from_date", "reqd", 0, "Check")
    make_property_setter('Leave Application', "to_date", "reqd", 0, "Check")
    make_property_setter('Leave Application', "from_date", "mandatory_depends_on", 'eval: !in_list(["Permission", "On Duty", ''], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "to_date", "mandatory_depends_on", 'eval: !in_list(["Permission", "On Duty", ''], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "from_date", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "to_date", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "half_day", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    
    
def create_custom_fields_():
    custom_field = {
        'Leave Application':[
            dict(
                fieldname='from_time', label='From Time', fieldtype='Time', insert_after='to_date', 
                mandatory_depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)'
            ),
            dict(
                fieldname='to_time', label='To Time', fieldtype='Time', insert_after='from_time', 
                mandatory_depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)'
            )
        ]
    }
    create_custom_fields(custom_field)