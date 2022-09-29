# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

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
            "label": _("Code"),
            "fieldtype": "Data",
            "fieldname": "code",
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

            "label": i,
            "fieldtype": "Float",
            "fieldname": i,
            "width": 100
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
            "label": _("Tiffen"),
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
            "width": 200
        },
        {
            "label": _("Signature"),
            "fieldtype": "Data",
            "fieldname": "signature",
            "width": 200
        }
    ]
    return columns
  

def get_data(filters):
    data=[]

    filter={'start_date':["<=", filters['from_date']],"end_date":[">=", filters['to_date']],'docstatus':1}
    keys = list(filters.keys())
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))
    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
    if ("designation" in keys):
        filter["designation"] = filters["designation"]
    ss=frappe.db.get_all("Salary Slip", filters=filter, fields=["employee","employee_name", "sum(total_shift_worked) as total_shift_worked","sum(net_pay) as net_pay","designation"],group_by="employee", order_by="designation")

    for j in ss:
        f=frappe._dict()
        get_ssa=frappe.db.get_all("Salary Structure Assignment", filters={'employee':j.employee, 'docstatus':1}, pluck='base')
        f.update({"designation":j.designation ,"code":j['employee'],"worker_name":j.employee_name,"salary":sum(get_ssa)})

        for k in between_dates:
            get_attendance=frappe.db.get_value("Attendance", {'employee':j.employee, 'docstatus':1,'attendance_date':k}, 'total_shift_count')
            f.update({k:get_attendance})
            
        f.update({"total_shift":j.total_shift_worked,"total_amount":j.net_pay,"tiffen":'',"pf_deduction":'',"esi_deduction":'',"total_deduction":'',"net_salary":j.net_pay,"signature":''})
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

