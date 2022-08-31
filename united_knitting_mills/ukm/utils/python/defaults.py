import frappe

def create_defults():
    create_role()
    create_leave_type()

def create_role():
    if(not frappe.db.exists('Role', 'Owner')):
        role = frappe.new_doc('Role')
        role.role_name = 'Owner'
        role.save()
        
def create_leave_type():
    if(not frappe.db.exists('Leave Type', 'Permission')):
        doc = frappe.new_doc('Leave Type')
        doc.leave_type_name = 'Permission'
        doc.insert()
    if(not frappe.db.exists('Leave Type', 'On Duty')):
        doc = frappe.new_doc('Leave Type')
        doc.leave_type_name = 'On Duty'
        doc.insert()