import frappe
def on_submit(doc,event):
    if doc.ref_doctype =="Employee Advance":
        employee_advance = frappe.get_doc("Employee Advance",doc.ref_docname)
        if employee_advance.status in ["Paid","Unpaid","Claimed","Returned","Partly Claimed and Returned"]:
            employee_advance.status = "Approved"
            employee_advance.save()
            employee_advance.submit()
            frappe.db.commit()