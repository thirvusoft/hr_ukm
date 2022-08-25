import frappe

def create_defults():
    create_role()

def create_role():
    if(not frappe.db.exists('Role', 'Owner')):
        role = frappe.new_doc('Role')
        role.role_name = 'Owner'
        role.save()