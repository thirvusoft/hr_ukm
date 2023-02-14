# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

# import frappe


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
    frappe.publish_realtime('refresh-report')
    return columns, data

def get_columns(filters):
    columns = [
         {
            "label": _("S.No"),
            "fieldtype": "Data",
            "fieldname": "sno",
            "width": 50
        },
        {
            "label": _("Employee ID"),
            "fieldtype": "Link",
            "fieldname": "code",
            "options":"Employee",
            "width": 110
        },
        {
            "label": _("Name of Employee"),
            "fieldtype": "Data",
            "fieldname": "worker_name",
            "width": 100
        },
        {
            "label": _("Designation"),
            "fieldtype": "Data",
            "fieldname": "designation",
            "width": 100
        },
        
        {
            "label": _("Salary"),
            "fieldtype": "Currency",
            "fieldname": "salary",
            "width": 80
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
        }),
  

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
       
    ]
    return columns
def get_data(filters):
    data=[]
    from_date = filters["from_date"]
    to_date = filters["to_date"]

    filter = {'attendance_date':["between", (from_date, to_date)],'docstatus':1}
    
    keys = list(filters.keys())

    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))

    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
   
    if ("designation" in keys):
        filter["designation"] = filters["designation"]

    if ("department" in keys):
        filter["department"] = filters["department"]

    if ("unit" in keys):
        filter["unit"] = filters["unit"]

    attendance=frappe.db.get_all("Attendance", filters=filter, fields=["name","employee","employee_name","designation","unit", "total_shift_count", "total_shift_amount", "sunday_attendance", "sunday_approval"], 
    group_by="employee",
    order_by="designation")
    no=1
    for j in attendance:
        f=frappe._dict()
        get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':j.employee, 'docstatus':1}, 'base')
        
        f.update(
            {   "sno":str(no),
                "code" : j['employee'],
                "worker_name":j.employee_name,
                "designation" : j.designation,
                "salary":get_ssa,
                
            }
        )
        shift=0
        shift_amount=0
        for k in between_dates:
            sunday_attendance = frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'sunday_attendance')
            sunday_approval = frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'sunday_approval')
            if not sunday_attendance or sunday_approval:
                get_attendance=frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'total_shift_count')
                get_amount=frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'total_shift_amount')
                f.update({k:get_attendance})
                shift=shift+(get_attendance or 0)
                shift_amount=shift_amount+(get_amount or 0)
        f.update({"total_shift":shift, "total_amount":shift_amount})
        data.append(f)
        no+=1   
    return data

