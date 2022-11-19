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
    
        
