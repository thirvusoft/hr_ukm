import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def attendance_customisation():
    attendance_property_setter()
    create_custom_fields()
   
def attendance_property_setter():
    attendance=frappe.get_doc({
        'doctype':'Property Setter',  
        'doctype_or_field': "DocField", 
        'doc_type': "Attendance", 
        'property':"options", 
        "property_type":"Select", 
        'field_name':"status", 
        "value":" \nPresent\nAbsent\nOn Leave\nHalf Day\nWork From Home\nQuater Day\nThree Quarter Day\nOne Quarter Day\nOne Half Day"     
    })       
    attendance.insert() 
    attendance.save(ignore_permissions=True) 
def create_custom_fields():
    pass