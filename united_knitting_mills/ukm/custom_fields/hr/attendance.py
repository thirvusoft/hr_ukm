import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def attendance_customisation():
    attendance_property_setter()
    create_attendance_custom_fields()
   
def attendance_property_setter():
    attendance=frappe.get_doc({
        'doctype':'Property Setter',  
        'doctype_or_field': "DocField", 
        'doc_type': "Attendance", 
        'property':"options", 
        "property_type":"Select", 
        'field_name':"status", 
        "value":" \nPresent\nAbsent\nOn Leave\nHalf Day\nWork From Home\nQuarter Day\nThree Quarter Day\nOne Quarter Day\nOne Half Day"     
    })       
    attendance.insert() 
    attendance.save(ignore_permissions=True)
    make_property_setter("Attendance", "status", "hidden", 1, "Check")
    make_property_setter("Attendance", "status", "hidden", 1, "Check")
    make_property_setter("Attendance", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Attendance", "company", "hidden", 1, "Check")
    make_property_setter("Attendance", "naming_series", "default", "HR-ATT-.YYYY.-", "Text")
    make_property_setter("Attendance", "naming_series", "hidden", 1, "Check")
    make_property_setter("Attendance", "late_entry", "read_only", 1, "Check")
    make_property_setter("Attendance", "early_exit", "read_only", 1, "Check")
    make_property_setter("Attendance", "shift", "hidden", 1, "Link")
    make_property_setter("Attendance", "employee", "read_only", 1, "Link")
    make_property_setter("Attendance", "attendance_date", "read_only", 1, "Date")




def create_attendance_custom_fields():
    custom_fields = {
		"Attendance": [
			
        dict(fieldname='shift_details', label='',
				fieldtype='Section Break',insert_after='exit_period'),
        
        dict(fieldname='employee_shift_details', label='Shift Approval List',
            fieldtype='Table',options='Thirvu Employee Checkin Details',insert_after='shift_details',read_only=1),

        dict(fieldname='thirvu_shift_details', label='Employee Shift',
            fieldtype='Table',options='Thirvu Attendance Shift Details',insert_after='employee_shift_details',hidden=1),

        dict(fieldname='unit', label='Unit',reqd=1,
			fieldtype='Link',options='Location',insert_after='employee_name',fetch_from='employee.location',read_only=1),
		
        dict(fieldname='designation', label='Designation',reqd=1,
			fieldtype='Link',options='Designation',insert_after='unit',fetch_from='employee.designation',read_only=1),
        
        dict(fieldname='staff', label='',
            fieldtype='Check',insert_after='employee',hidden=1),

        dict(fieldname='mismatched_checkin', label='Mismatched Checkin',
            fieldtype='Check',insert_after='reason',read_only=1),
        
        dict(fieldname='no_of_checkin', label='Checkin Count',
            fieldtype='Data',insert_after='mismatched_checkin',depends_on='eval:doc.mismatched_checkin',read_only=1),
        
        dict(fieldname='insufficient_working_minutes', label='Insufficient Working Minutes',
            fieldtype='Check',insert_after='no_of_checkin',read_only=1),
        
        dict(fieldname='insufficient_working_hrs', label='Actual Worked (Hours)',
            fieldtype='Float',insert_after='insufficient_working_minutes',depends_on='eval:doc.insufficient_working_minutes',read_only=1),

        dict(fieldname='break_time_overconsumed', label='Breaktime Overconsumed',
            fieldtype='Check',insert_after='insufficient_working_hrs',read_only=1),

        dict(fieldname='over_consumed_time', label='Consumed Minutes (Break Time)',
            fieldtype='Float',insert_after='break_time_overconsumed',depends_on='eval:doc.break_time_overconsumed',read_only=1),

        dict(fieldname='action_taken_by_hr', label='Action Taken By HR',
            fieldtype='Small Text',insert_after='over_consumed_time',mandatory_depends_on='eval:doc.break_time_overconsumed || doc.late_entry || doc.early_exit || doc.mismatched_checkin || doc.insufficient_working_minutes'),
       
        dict(fieldname='late_min', label='Consumed Minutes (Late Entry)',
            fieldtype='Float',depends_on='eval:doc.late_entry',insert_after='late_entry',read_only=1),
        
        dict(fieldname='exit_period', label='Early Exit (in Minutes)',
            fieldtype='Float',insert_after='early_exit', depends_on = "eval:doc.early_exit",read_only=1),
        
        dict(fieldname='time_sc_br', label='',
            fieldtype='Section Break',insert_after='thirvu_shift_details'),

        dict(fieldname='checkin_time', label='Check-In Time',
            fieldtype='Time',insert_after='time_sc_br',read_only=1),
        
        dict(fieldname='time_cl_br', label='',
            fieldtype='Column Break',insert_after='checkin_time'),

        dict(fieldname='checkout_time', label='Check-Out Time',
            fieldtype='Time',insert_after='time_cl_br',read_only=1),
        
        dict(fieldname='section_break23', label='',
        fieldtype='Section Break',insert_after='checkout_time'),

        dict(fieldname='total_shift_hr', label='Total Shift in Minutes',
        fieldtype='Float',insert_after='section_break23',read_only=1),          
        
        dict(fieldname='column_break24', label='',
        fieldtype='Column Break',insert_after='total_shift_hr'),       

        dict(fieldname='total_shift_count', label='Total Shift Count',
        fieldtype='Float',insert_after='column_break24',depends_on='eval:!doc.staff',read_only=1),

        dict(fieldname='ts_ot_hrs', label='Extra Time Taken in Minutes',
        fieldtype='Float',insert_after='total_shift_count',depends_on='eval:doc.staff',read_only=1), 

        dict(fieldname='column_break23', label='',
        fieldtype='Column Break',insert_after='ts_ot_hrs'),

        dict(fieldname='total_shift_amount', label='Amount to Pay',
        fieldtype='Currency',insert_after='column_break23',read_only=1),

        # Requested change fields
        dict(fieldname='req_section_break23', label='',
        fieldtype='Section Break',insert_after='total_shift_amount',depends_on='eval:doc.docstatus == 0'),

        dict(fieldname='req_total_shift_hr', label='Requested Shift in Minutes',
        fieldtype='Float',insert_after='req_section_break23'),           
        
        dict(fieldname='req_column_break24', label='',
        fieldtype='Column Break',insert_after='req_total_shift_hr'),
        
        dict(fieldname='req_ts_ot_hrs', label='Requested Extra Time in Minutes',
        fieldtype='Float',insert_after='req_column_break24',depends_on='eval:doc.staff'), 
        
        dict(fieldname='req_total_shift_count', label='Requested Shift Count',
        fieldtype='Float',insert_after='req_ts_ot_hrs',depends_on='eval:!doc.staff'),
        
        dict(fieldname='req_column_break23', label='',
        fieldtype='Column Break',insert_after='req_total_shift_count'),

        dict(fieldname='req_total_shift_amount', label='Requested Amount to Pay',
        fieldtype='Currency',insert_after='req_column_break23',read_only_depends_on='eval:!doc.staff'),
        
        dict(fieldname='reason', label='Reason for Draft',
        fieldtype='Small Text',insert_after='out_time', read_only=1,hidden=1),

        
      
         ]
    }
    create_custom_fields(custom_fields)