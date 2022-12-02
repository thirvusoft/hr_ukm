import frappe
import json
from frappe.model.document import Document

class EmployeeBonusTool(Document):
    pass



@frappe.whitelist()
def employee_finder(designation,location,from_date,to_date):
    settings = frappe.get_single("United Knitting Mills Settings")
    employee_names=[]
    amount=[]
    working_days = []
    table=[]
    emp_list=frappe.get_all("Employee",filters={"designation" : designation,'location' : location},fields=["name", "employee_name","designation"],order_by="name")
    print(emp_list)
    thirvu_shift=frappe.get_value("Employee Timing Details", designation, 'staff')
    for name in emp_list:
        attendance_status=0
        bonus_percent= bonus_on_days(name['name'])
        if thirvu_shift==1:
            attendance_status = frappe.db.sql("""
                    SELECT count(att.name)
                    FROM `tabAttendance` as att
                    WHERE  att.employee = '{0}' and att.attendance_date between '{1}' and '{2}' and att.workflow_state = 'Present' and att.docstatus = 1
                    """.format(name['name'],from_date,to_date),as_list=1)[0][0]
        else:
            attendance_status = frappe.db.sql(f"""
                    SELECT count(att.name)
                    FROM `tabAttendance` as att
                    WHERE  att.employee = '{name['name']}' and att.attendance_date between '{from_date}' and '{to_date}' and 
                    att.checkin_time <= '{settings.from_time}' and 
                    att.checkout_time >= '{settings.to_time}' and
                    att.workflow_state = 'Present' and att.docstatus = 1
                    """,as_list=1)[0][0]
            
      
        emp_base_amount=frappe.db.sql("""select ssa.base
                FROM `tabSalary Structure Assignment` as ssa
                WHERE ssa.employee = '{0}' and ssa.from_date <='{1}'
                ORDER BY ssa.from_date DESC LIMIT 1 """.format(name['name'],to_date),as_list=1)
        print(emp_base_amount, name['name'], attendance_status)
        calc=0
        if emp_base_amount:
            calc = (float(attendance_status) * float(emp_base_amount[0][0])) * ( bonus_percent/ 100)
            amount.append(calc)
            working_days.append(attendance_status)
            employee_names.append(name)
        table.append({'employee':name['name'],'employee_name':name['employee_name'],'designation':designation,'working_days':attendance_status,'current_bonus':calc})
    return employee_names, amount, working_days, table

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

def bonus_on_days(name):
    count=0
    settings = frappe.get_single("United Knitting Mills Settings")
    attedance=frappe.db.get_all("Attendance", filters={'employee':name, 'status':'Present'}, fields=['employee'])
    count=len(attedance)
    for j in range(0, len(settings.bonus_table), 1):
        for k in range(j, len(settings.bonus_table), 1):
            if settings.bonus_table[j].days_allowed_for_bonus <= count >= settings.bonus_table[k].days_allowed_for_bonus :
               return settings.bonus_table[k].bonus_percentage
                 
    return 0            