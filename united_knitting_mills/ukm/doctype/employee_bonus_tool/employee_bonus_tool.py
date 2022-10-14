import frappe
import json
from frappe.model.document import Document

class EmployeeBonusTool(Document):
    pass



@frappe.whitelist()
def employee_finder(designation,location,from_date,to_date):
    employee_names=[]
    amount=[]
    working_days = []
    emp_list=frappe.db.get_all("Employee",filters={"designation" : designation,'location' : location},fields=["name", "employee_name"],order_by="name")
    bonus_percent= frappe.db.get_single_value("United Knitting Mills Settings", "bonus_percentage")
    for name in emp_list:
        attendance_status = frappe.db.sql("""
            SELECT count(att.name)
            FROM `tabAttendance` as att
            WHERE  att.employee = '{0}' and att.attendance_date between '{1}' and '{2}' and att.status = 'Present' and att.docstatus = 1
            """.format(name['name'],from_date,to_date),as_list=1)[0][0]

        emp_base_amount=frappe.db.sql("""select ssa.base
                FROM `tabSalary Structure Assignment` as ssa
                WHERE ssa.employee = '{0}' and ssa.from_date <='{1}'
                ORDER BY ssa.from_date DESC LIMIT 1 """.format(name['name'],to_date),as_list=1)
        
        if emp_base_amount:
            calc = (float(attendance_status) * float(emp_base_amount[0][0])) * ( bonus_percent/ 100)

            amount.append(calc)
            working_days.append(attendance_status)
        employee_names.append(name)
        
    return employee_names, amount, working_days

@frappe.whitelist()
def total_bonus_amt_total(doc,event):
    total_bonus_amt = 0
    for bonus_list in doc.employee_bonus_details:
        if bonus_list.current_bonus:
            total_bonus_amt += bonus_list.current_bonus
    doc.total_bonus_amount =  total_bonus_amt



@frappe.whitelist()
def create_bonus(doc,event):
    
    for bonus_list in doc.employee_bonus_details:
        if bonus_list.current_bonus:
            bonus_doc=frappe.new_doc('Employee Bonus')
            bonus_doc.employee = bonus_list.employee
            bonus_doc.bonus_amount = bonus_list.current_bonus
            bonus_doc.bonus_payment_date = doc.date
            bonus_doc.reference = doc.name
            bonus_doc.bonus_account = doc.bonus_account
            
            bonus_doc.save()
            bonus_doc.submit()
    



