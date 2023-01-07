import frappe

@frappe.whitelist()
def advance_validation(employee, from_date, to_date):
   
    emp_shift_amount = frappe.db.sql("""
                         select sum(total_shift_amount), sum(total_shift_count)
                         from `tabAttendance`
                         where employee=%s and attendance_date>=%s and attendance_date<=%s and docstatus = 1
		        """, (employee, from_date, to_date), as_list = 1)
    
    if emp_shift_amount:
        return emp_shift_amount[0][0], emp_shift_amount[0][1]

def employee_advance_cancel(doc, event):
    pe=frappe.get_all("Payment Entry", filters=[["docstatus", '=', 1], ['Payment Entry Reference', 'reference_name', '=', doc.name]] , pluck='name' )
    for i in pe:
        pe_doc=frappe.get_doc("Payment Entry", i)
        pe_doc.cancel()
    doc.ignore_linked_doctypes = ("GL Entry")

def employee_advance_delete(doc, event):
    pe=frappe.get_all("Payment Entry", filters=[["docstatus", '!=', 1], ['Payment Entry Reference', 'reference_name', '=', doc.name]] , pluck='name' )
    for i in pe:
       frappe.delete_doc("Payment Entry", i)

def additional_salary_cancel(doc, event):
    as_doc=frappe.get_all("Additional Salary", filters={"docstatus":1, "ref_docname":doc.name} , pluck='name' )
    for i in as_doc:
        additon_salary=frappe.get_doc("Additional Salary", i)
        additon_salary.cancel()
def additional_salary_delete(doc, event):
    additional_salary=frappe.get_all("Additional Salary", filters={"docstatus":["!=", 1], "ref_docname":doc.name}, pluck='name' )
    for i in additional_salary:
       frappe.delete_doc("Additional Salary", i)
        
