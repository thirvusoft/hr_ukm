import frappe
def workflow_document_creation():
    create_roles()
    create_state()
    create_action()
    create_workflow_doc()
    workflow_attendance()

def create_workflow_doc():
    if frappe.db.exists('Workflow', 'Salary Structure'):
        frappe.delete_doc('Workflow', 'Salary Structure')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Salary Structure'
    workflow.document_type = 'Salary Structure'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1

    workflow.append('states', dict(
        state = 'Approval Pending',doc_status=0, allow_edit = 'Thirvu HR User'
    ))
    workflow.append('states', dict(
        state = 'Approval Pending',doc_status=0, allow_edit = 'Thirvu HR Manager'
    ))
    workflow.append('states', dict(
        state = 'Approved by Owner',doc_status=1, allow_edit = 'Thirvu Owner'
    ))
    workflow.append('states', dict(
        state = 'Rejected by Owner',doc_status=0, allow_edit = 'Thirvu Owner'
    ))

    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Approve', next_state = 'Approved by Owner',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))
    workflow.append('transitions', dict(
        state = 'Approval Pending', action='Reject', next_state = 'Rejected by Owner',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list=["Draft","Submitted","Rejected",'Approval Pending','Approved by Owner','Rejected by Owner','Pending Approval for Absent','Pending Approval for Present','Approval for Present','Approval for Absent','Present','Absent']
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            if(row=="Draft"):
                new_doc.style="Warning"
            if(row=="Submitted"):
                new_doc.style="Success"
            if(row=="Rejected"):
                new_doc.style="Danger"
            if(row=="Approved by Owner"):
                new_doc.style="Success"
            if(row=="Approval Pending"):
                new_doc.style="Warning"
            if(row=="Rejected by Owner"):
                new_doc.style="Danger"
            if(row=="Present"):
                new_doc.style="Success"
            if(row=="Absent"):
                new_doc.style="Danger"
            if(row=="pending Approval for Absent"):
                new_doc.style="Warning"
            if(row=="pending Approval for Present"):
                new_doc.style="Primary"
            new_doc.save()

def create_action():
    list=["Reject", "Submit", "Draft",'Approve', 'Action','Send Approval for Present','Send Approval for Absent','Approval for Present','Approval for Absent']
    for row in list:
        if not frappe.db.exists('Workflow Action Master', row):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = row
            new_doc.save()

def create_roles():
    role_list = ['Thirvu Owner','Thirvu HR User','Thirvu HR Manager']
    for role in role_list:
        if not frappe.db.exists("Role",role):
            role = frappe.get_doc({'doctype':'Role', 'role_name':role}).insert()
        
   


def workflow_attendance():
    if frappe.db.exists('Workflow', 'Attendance'):
        frappe.delete_doc('Workflow', 'Attendance ')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Attendance '
    workflow.document_type = 'Attendance '
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1

    workflow.append('states', dict(
        state = 'Draft',doc_status=0, allow_edit = 'Thirvu HR User'
    ))
    workflow.append('states', dict(
        state = 'Pending Approval for Present',doc_status=0, allow_edit = 'Thirvu HR User'
    ))
    workflow.append('states', dict(
        state = 'Pending Approval for Absent',doc_status=0, allow_edit = 'Thirvu HR Manager'
    ))
    workflow.append('states', dict(
        state = 'Approval for Present',doc_status=0, allow_edit = 'Thirvu Owner'
    ))
    workflow.append('states', dict(
        state = 'Approval for Absent',doc_status=0, allow_edit = 'Thirvu Owner'
    ))
    workflow.append('states', dict(
        state = 'Present',doc_status=1, allow_edit = 'Thirvu Owner'
    ))
    workflow.append('states', dict(
        state = 'Absent',doc_status=1, allow_edit = 'Thirvu Owner'
    ))
  

    workflow.append('transitions', dict(
        state = 'Draft', action='Send Approval for Present', next_state = 'Pending Approval for Present',
        allowed='Thirvu HR User', allow_self_approval= 1,condition='doc.action_taken_by_hr'
    ))
    workflow.append('transitions', dict(
        state = 'Draft', action='Send Approval for Absent', next_state = 'Pending Approval for Absent',
        allowed='Thirvu HR User', allow_self_approval= 1,condition='doc.action_taken_by_hr'
    ))
    workflow.append('transitions', dict(
        state = 'Pending Approval for Present', action='Approval for Present', next_state = 'Present',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))
    workflow.append('transitions', dict(
        state = 'Pending Approval for Absent', action='Approval for Absent', next_state = 'Absent',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))

    workflow.append('transitions', dict(
        state = 'Pending Approval for Present', action='Approval for Absent', next_state = 'Absent',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))
    workflow.append('transitions', dict(
        state = 'Pending Approval for Absent', action='Approval for Present', next_state = 'Present',
        allowed='Thirvu Owner', allow_self_approval= 1
    ))

    workflow.insert(ignore_permissions=True)
    return workflow

