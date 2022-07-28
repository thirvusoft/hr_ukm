import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
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
def create_attendance_custom_fields():
    custom_fields = {
		"Attendance": [
			dict(fieldname='shift_details', label='',
				fieldtype='Section Break',insert_after='early_exit'),

			dict(fieldname='thirvu_shift_details', label='Employee Shift',
				fieldtype='Table',options='Thirvu Attendance Shift Details',insert_after='employee_shift_details'),
            
            dict(fieldname='total_shift_count', label='Total Shift Count',
				fieldtype='Float',insert_after='column_break24'),
            
            dict(fieldname='total_shift_hr', label='Total Shift Hour',
				fieldtype='Float',insert_after='section_break23'),
           
            dict(fieldname='employee_shift_details', label='Shift Approval List',
				fieldtype='Table',options='Thirvu Employee Checkin Details',insert_after='shift_details',read_only=1),
            
            dict(fieldname='section_break23', label='',
				fieldtype='Section Break',insert_after='thirvu_shift_details'),
           
            dict(fieldname='column_break24', label='',
				fieldtype='Column Break',insert_after='total_shift_hr'),
            
            dict(fieldname='thirvu_reason', label='Reason',
				fieldtype='Data',depends_on='eval:doc.late_entry',mandatory_depends_on='eval:doc.late_entry',insert_after='late_entry'),
           
            dict(fieldname='column_break23', label='',
				fieldtype='Column Break',insert_after='total_shift_count'),
            
            dict(fieldname='total_shift_amount', label='Total Shift Amount',
				fieldtype='Currency',insert_after='column_break23'),
            ]
    }
    create_custom_fields(custom_fields)