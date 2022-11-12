# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

from ctypes.wintypes import PFLOAT
import frappe
import pandas
from datetime import date, datetime, timedelta
from frappe import _
from erpnext.education.report.student_monthly_attendance_sheet.student_monthly_attendance_sheet import daterange

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Designation"),
            "fieldtype": "Data",
            "fieldname": "designation",
            "width": 100
        },
        {
            "label": _("ID"),
            "fieldtype": "Link",
            "fieldname": "code",
            "options":"Employee",
            "width": 100
        },
        {
            "label": _("Worker Name"),
            "fieldtype": "Data",
            "fieldname": "worker_name",
            "width": 100
        },
        {
            "label": _("Salary"),
            "fieldtype": "Currency",
            "fieldname": "salary",
            "width": 100
        },
      
        ]
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))
    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
    for i in between_dates:
        
        columns.append({

            "label": i[len(i)-2:],
            "fieldtype": "Float",
            "fieldname": i,
            "print_width": 10
        })
    columns+=[
        {
            "label": _("Total Shift"),
            "fieldtype": "Float",
            "fieldname": "total_shift",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "fieldname": "total_amount",
            "width": 100
        },
        {
            "label": _("Advance"),
            "fieldtype": "Currency",
            "fieldname": "advance",
            "width": 100
        },
        {
            "label": _("Food Expense"),
            "fieldtype": "Currency",
            "fieldname": "tiffen",
            "width": 100
        },
        {
            "label": _("PF Deduction"),
            "fieldtype": "Currency",
            "fieldname": "pf_deduction",
            "width": 100
        },
        {
            "label": _("ESI Deduction"),
            "fieldtype": "Currency",
            "fieldname": "esi_deduction",
            "width": 100
        },
        {
            "label": _("Total Deduction"),
            "fieldtype": "Currency",
            "fieldname": "total_deduction",
            "width": 100
        },
        {
            "label": _("Net Salary"),
            "fieldtype": "Currency",
            "fieldname": "net_salary",
            "width": 100
        },
        {
            "label": _("Signature"),
            "fieldtype": "Data",
            "fieldname": "signature",
            "width": 200
        },
        {
            "label": _("From Date"),
            "fieldtype": "Data",
            "fieldname": "from_date",
            "width": 200,
            "hidden":1
        },
        {
            "label": _("To Date"),
            "fieldtype": "Data",
            "fieldname": "to_date",
            "width": 200,
            "hidden":1
        }
    ]
    return columns
  

def get_data(filters):
    data=[]

    # filter={'start_date':["<=", filters['from_date']],"end_date":[">=", filters['to_date']],'docstatus':1}
    filter={'start_date':["<=", filters['from_date']],"end_date":[">=", filters['to_date']]}
    keys = list(filters.keys())
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))
    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
    if ("designation" in keys):
        filter["designation"] = filters["designation"]
    if ("department" in keys):
        filter["department"] = filters["department"]
    if ("unit" in keys):
        filter["unit"] = filters["unit"]
    ss=frappe.db.get_all("Salary Slip", filters=filter, fields=["name","employee","employee_name", "total_shift_worked","net_pay", "total_deduction","designation"],group_by="employee", order_by="designation")
    for j in ss:
        f=frappe._dict()
        get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':j.employee, 'docstatus':1}, 'base')
        f.update({"designation":j.designation ,"code":j['employee'],"worker_name":j.employee_name,"salary":get_ssa})

        for k in between_dates:
            get_attendance=frappe.db.get_value("Attendance", {'employee':j.employee, 'docstatus':1,'attendance_date':k}, 'total_shift_count')
            f.update({k:get_attendance})

        salary_slip_detail=frappe.get_doc("Salary Slip",j.name)
        food_expence_count = 0
        pf_count = 0
        esi_count = 0
        advance_count = 0
        advance = "" 
        food_expence = ""
        esi = ""
        pf = ""
        for x in range(0,len(salary_slip_detail.deductions),1):
            if food_expence_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Food Expense":
                    food_expence = salary_slip_detail.deductions[x].__dict__["amount"]
                    food_expence_count = 1

            if esi_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "ESI":
                    esi = salary_slip_detail.deductions[x].__dict__["amount"]
                    esi_count = 1

            if pf_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "PF":
                    pf = salary_slip_detail.deductions[x].__dict__["amount"]
                    pf_count = 1
 
            if advance_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Employee Advance":
                    advance = salary_slip_detail.deductions[x].__dict__["amount"]
                    advance_count = 1

        f.update({"total_shift":j.total_shift_worked,"total_amount":j.net_pay,"advance":advance,"tiffen":food_expence,"pf_deduction":pf,"esi_deduction":esi,"total_deduction":j.total_deduction,"net_salary":j.net_pay,"signature":'',"from_date":filters["from_date"],'to_date':filters["to_date"]})
        data.append(f)
    d = [list(i.values()) for i in data]
   
    check =''
    for i in range (0,len(d),1):
        if d[i][0] != check:
            check = d[i][0] 
            d[i][0] = f'<b>{d[i][0]}</b>'
           
        else:
            d[i][0]=''
   
    return d

