import frappe
import json
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils import getdate, now_datetime, nowdate


class EmployeeBonusTool(Document):
    def on_cancel(self):
        bonus_cancel=frappe.get_all("Employee Bonus", filters={"docstatus":["=", 1], "reference":self.name} , pluck='name' )
        for i in bonus_cancel:
            ea_doc=frappe.get_doc("Employee Bonus", i)
            ea_doc.cancel()

    def on_trash(self):
        employee_bonus=frappe.get_all("Employee Bonus", filters={"docstatus":["!=", 1], "reference":self.name}, pluck='name' )
        for i in employee_bonus:
            frappe.delete_doc("Employee Bonus", i)


@frappe.whitelist()
def employee_finder(emp_department=None,designation=None,location=None,from_date=None,to_date=None):
    settings = frappe.get_single("United Knitting Mills Settings")
    bonuspercentage = settings.bonus_percentage
    table=[]
    filters={}
    if emp_department:
        filters["department"] = emp_department
    if location:
        filters['location'] = location
    if designation:
        filters['designation'] = designation
    emp_list=frappe.get_all("Employee",filters=filters, fields=["name", "employee_name","department",'designation', 'location'],order_by="name")

    from_date = getdate(from_date)
    to_date = getdate(to_date)
    difference_in_months = float(relativedelta(to_date, from_date).months)
    for name in emp_list:
        unused_pay_leaves=0
        payleave_salary=0
        get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':name.name, 'docstatus':1, 'workflow_state':"Approved by MD"}, 'base') or 0
        department_staff=frappe.get_value("Department", name.department, "is_staff")
        if department_staff == 0:
            employee_bonus = frappe.db.sql(f"""
                SELECT
                    esd.from_date,
                    esd.to_date,
                    CASE
                        WHEN (SELECT dep.is_staff FROM `tabDepartment` dep WHERE dep.name = esd.deparment limit 1) = 1
                            THEN esd.base / (TIMESTAMPDIFF(DAY, esd.from_date ,  DATE_ADD(esd.to_date, INTERVAL 1 DAY)))
                        ELSE
                            esd.base
                    END base, 
                    (
                        SELECT 
                            count(att.name)
                        FROM `tabAttendance` as att
                        WHERE  
                            att.employee = '{name['name']}' and 
                            att.attendance_date between GREATEST('{from_date}', esd.from_date) and LEAST('{to_date}', esd.to_date) and 
                            att.total_shift_count >= 1 and  DATE_FORMAT(att.attendance_date, '%W') != 'Sunday' and
                            CASE
                                WHEN (SELECT dep.is_staff FROM `tabDepartment` dep WHERE dep.name = att.department limit 1) = 1
                                    THEN 1
                                WHEN (SELECT emp.location FROM `tabEmployee` emp WHERE emp.name = att.employee ) = 'UNIT 1'
                                    THEN (
                                            att.checkin_time <= '{settings.from_time}' and 
                                            CASE
                                                WHEN att.checkout_time <= '23:59:59'
                                                THEN att.checkout_time >= '{settings.to_time}'
                                                ELSE 1
                                            END
                                        )
                                WHEN (SELECT emp.location FROM `tabEmployee` emp WHERE emp.name = att.employee) = 'UNIT 2'
                                    THEN (
                                            att.checkin_time <= '{settings.from_time_unit_2}' and 
                                            CASE
                                                WHEN att.checkout_time <= '23:59:59'
                                                THEN att.checkout_time >= '{settings.to_time_unit_2}'
                                                ELSE 1
                                            END
                                        )
                            END and
                            att.workflow_state = 'Present' and 
                            att.docstatus = 1
                    ) days
                FROM `tabEmployee Salary Details` esd
                WHERE
                    esd.employee = '{name['name']}' AND
                    esd.docstatus = 1 AND
                    esd.workflow_state = 'Approved by MD' AND
                    (
                        (esd.from_date BETWEEN '{from_date}' AND '{to_date}' OR esd.to_date BETWEEN '{from_date}' AND '{to_date}')
                        OR ('{from_date}' BETWEEN esd.from_date AND esd.to_date OR '{to_date}' BETWEEN esd.from_date AND esd.to_date)
                    )
            """, as_dict = True, debug=1)
            salary = sum([(bonus.days or 0) * (bonus.base or 0) for bonus in employee_bonus])
            bonus_amt = ((bonuspercentage or 0) / 100) * salary
            days = sum([(bonus.days or 0) for bonus in employee_bonus])
            leavedays = days/32 or 0.00
            settlementdays=days/22 or 0
            total_amount=bonus_amt+(leavedays*(get_ssa or 0) or 0)+(settlementdays*(get_ssa or 0) or 0)
        else:
            employee_bonus = frappe.db.sql(f""" 
                SELECT
                    ss.total_working_days,
                    ss.payment_days,
                    ss.absent_days,
                    ss.leave_with_pay,
                    ss.gross_pay
                FROM `tabSalary Slip` ss
                WHERE
                    ss.employee = '{name['name']}' AND
                    ss.docstatus = 1 AND
                    ss.unit = '{name['location']}' AND
                    ss.start_date between '{from_date}' AND '{to_date}' and
                    ss.end_date between '{from_date}' AND '{to_date}'
                    """, as_dict=1)
            pending_paid_leave_ss=frappe.db.sql(f"""
                                    SELECT
                                        ss.leave_with_pay,
                                        ss.per_day_salary_for_staff
                                    FROM `tabSalary Slip` ss
                                    WHERE
                                        ss.employee = '{name['name']}' AND
                                        ss.docstatus = 1 AND
                                        ss.unit = '{name['location']}' AND
                                        ss.start_date between '{from_date}' AND '{to_date}' and
                                        ss.end_date between '{from_date}' AND '{to_date}' and
                                        ss.leave_with_pay < {settings.pay_leave} and
                                        ss.total_working_days = ss.payment_days
                                        """, as_dict=True)
            pending_paid_leave_amt=sum([(settings.pay_leave-i.leave_with_pay)*i.per_day_salary_for_staff for i in pending_paid_leave_ss])
            pending_paid_leave_count=sum([(settings.pay_leave-i.leave_with_pay) for i in pending_paid_leave_ss])
                
            salary = sum([(bonus.gross_pay or 0) for bonus in employee_bonus])
            bonus_amt = ((bonuspercentage or 0) / 100) * salary
            days = sum([(bonus.payment_days or 0) for bonus in employee_bonus])
            leavedays = 0.00
            unused_pay_leaves=pending_paid_leave_count or 0
            payleave_salary=pending_paid_leave_amt or 0
            settlementdays= 0.00
            total_amount=bonus_amt+(payleave_salary or 0)
        table.append({
            'employee': name['name'],
            'employee_name': name['employee_name'],
            'designation': name['designation'],
            'working_days': days,
            'current_bonus': bonus_amt, 
            'salary': salary,
            'bonus_percentage': bonuspercentage,
            'leave_days' : leavedays,
            'leave_salary': (leavedays*(get_ssa or 0) or 0),
            'settlement_days':settlementdays,
            'settlement_salary' : (settlementdays*(get_ssa or 0) or 0),
            'unused_pay_leaves' : unused_pay_leaves or 0,
            'pay_leave_salary': payleave_salary or 0,
            'total_bonus_amount':total_amount,
        })
    return table


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
            bonus_doc.from_date = doc.from_date
            bonus_doc.to_date = doc.to_date
            bonus_doc.bonus_percentage = bonus_list.bonus_percentage
            bonus_doc.total_bonus_amount = bonus_list.current_bonus
            bonus_doc.working_days = bonus_list.working_days
            bonus_doc.total_salary_amount = bonus_list.salary
            bonus_doc.leave_days = bonus_list.leave_days
            bonus_doc.leave_salary = bonus_list.leave_salary
            bonus_doc.settlement_days = bonus_list.settlement_days
            bonus_doc.settlement_salary = bonus_list.settlement_salary
            bonus_doc.unused_pay_leaves = bonus_list.unused_pay_leaves
            bonus_doc.pay_leave_salary = bonus_list.pay_leave_salary
            bonus_doc.bonus_payment_date = doc.date
            bonus_doc.reference = doc.name
            bonus_doc.bonus_account = doc.bonus_account
            bonus_doc.bonus_amount = bonus_list.total_bonus_amount
            
            bonus_doc.save()
            bonus_doc.submit()

def bonus_on_days(name):
    count=0
    settings = frappe.get_single("United Knitting Mills Settings")
    days=[i.days_allowed_for_bonus for i in settings.bonus_table]
    days.sort()
    matched_day=days[-1] if len(days) else 0
    attedance=frappe.db.get_all("Attendance", filters={'employee':name, 'workflow_state':'Present'}, fields=['employee'])
    count=len(attedance)
    for i in range(len(days)):
        if count>days[i]:
            continue
        else:
            if i==0:
                matched_day=days[i]
            else:
                matched_day=days[i-1]
            break
   
    for j in settings.bonus_table:
        if j.days_allowed_for_bonus== matched_day:
            return j.bonus_percentage
    return 0            
