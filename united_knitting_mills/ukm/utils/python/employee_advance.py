from datetime import timedelta
import frappe
from frappe.utils import (add_days,nowdate,)
@frappe.whitelist()
def advance_validation(employee,from_date,to_date):
    # latest_salary_slip=frappe.get_all("Salary Slip",{"employee":employee,"docstatus":"1"},["name","end_date"],
    #                                 order_by="end_date desc",
    #                                 limit=1)
    # to_date=nowdate()
    # if latest_salary_slip:
    #     from_date=latest_salary_slip[0].end_date + timedelta(days=1)
    #     previous_advance=0
    #     previous_advance= frappe.db.sql("""select sum(advance_amount) from `tabEmployee Advance`
    #                                         where employee='{0}' and posting_date between '{1}' and '{2}' and docstatus IN ("0","1")
    #                                     """.format(employee,from_date,to_date),as_list=1)
    #     if previous_advance:
    #         previous_advance=previous_advance[0][0]
    #     emp_shift_amount = frappe.db.sql("""
    #                     select sum(total_shift_amount)
    #                     from `tabAttendance`
    #                     where employee=%s and attendance_date>=%s and attendance_date<=%s and docstatus = 1
	# 	        """, (employee,from_date,to_date), as_list = 1)
    #     if emp_shift_amount and previous_advance:
    #         return (emp_shift_amount[0][0] - previous_advance)
    #     elif emp_shift_amount:
    #         return (emp_shift_amount[0][0])
    # else:
    emp_shift_amount = frappe.db.sql("""
                         select sum(total_shift_amount)
                         from `tabAttendance`
                         where employee=%s and attendance_date>=%s and attendance_date<=%s and docstatus = 1
		        """, (employee,from_date,to_date), as_list = 1)
    
    if emp_shift_amount:
        return emp_shift_amount[0][0]
    
        
def validate(doc,event):
    if doc.advance_amount:
        if doc.eligible_amount:
            if doc.advance_amount > doc.eligible_amount:
                frappe.throw(f"Advance amount cannot be greater than {doc.eligible_amount}")
        else:
            frappe.throw(f"Employee {doc.employee} is not eligible for advance amount")
    else:
        frappe.throw(f"Advance amount cannot be 0")
