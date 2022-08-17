import frappe
def fetch_designation():
    checkin = frappe.get_all('Employee Checkin')
    for data in checkin:
        doc = frappe.get_doc('Employee Checkin',data)
        doc.designation = frappe.db.get_value('Employee', doc.employee, "designation")
        doc.save()