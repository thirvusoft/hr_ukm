import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def leave_application_customizations():
    leave_application_property_setter()
    leave_application_custom_fields_()
    
def leave_application_property_setter():
    make_property_setter('Leave Application', "from_date", "reqd", 0, "Check")
    make_property_setter('Leave Application', "to_date", "reqd", 0, "Check")
    make_property_setter('Leave Application', "from_date", "mandatory_depends_on", 'eval: !in_list(["Permission", "On Duty", ''], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "to_date", "mandatory_depends_on", 'eval: !in_list(["Permission", "On Duty", ''], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "from_date", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "to_date", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    make_property_setter('Leave Application', "half_day", "depends_on", 'eval: !in_list(["Permission", "On Duty"], doc.leave_type)', "Small Text")
    make_property_setter("Leave Application", "sb10", "hidden", 1, "Section Break")
    make_property_setter("Leave Application", "leave_approver", "hidden", 1, "Check")
    make_property_setter("Leave Application", "leave_approver_name", "hidden", 1, "Check")
    make_property_setter("Leave Application", "salary_slip", "hidden", 1, "Check")
    make_property_setter("Leave Application", "description", "reqd", 1, "Small Text")
    make_property_setter("Leave Application", "leave_balance", "hidden", 1, "Check")
    
def leave_application_custom_fields_():
    custom_field = {
        'Leave Application':[
            dict(
                fieldname='from_time', label='From Time', fieldtype='Time', insert_after='attendance_date', 
                mandatory_depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)'
            ),
            dict(
                fieldname='to_time', label='To Time', fieldtype='Time', insert_after='from_time', 
                mandatory_depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)'
            ),
            dict(
                fieldname='attendance_date', label='Date', fieldtype='Date', insert_after='to_date', 
                mandatory_depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)'
            ),
            dict(
                fieldname='attendance_marked', label='Attendance Marked', fieldtype='Check', hidden=1,insert_after='to_date', 
                depends_on='eval: in_list(["Permission", "On Duty"], doc.leave_type)',read_only=1,allow_on_submit=1
            ),
            dict(fieldname='unit', label='Unit',reqd=1,
				fieldtype='Link',options='Location',insert_after='employee_name',fetch_from='employee.location')
        ]
    }
    create_custom_fields(custom_field)