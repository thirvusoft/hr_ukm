# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns=get_columns(filters)
	data=get_data(filters)
	return columns, data


def get_columns(filters):
    from datetime import datetime, timedelta

    date1 = datetime.strptime(filters.get('from_date'), '%Y-%m-%d')
    date2 = datetime.strptime(filters.get('to_date'), '%Y-%m-%d')
    current_date = date1
   
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
            "fieldname": "employee",
            "options":"Employee",
            "width": 110
        },
        {
            "label": _("Name of Employee"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 100
        },
        {
            "label": _("Designation"),
            "fieldtype": "Data",
            "fieldname": "designation",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldtype": "Select",
            "fieldname": "status",
            "options":["", "Active", "Inactive", "Suspended", "Left"],
            "width": 100
        },
        {
            "label": _("Current Wages"),
            "fieldtype": "Float",
            "fieldname": "current_wages",
            "width": 100
        },
    ]
    
    while current_date <= date2:
        month = current_date.strftime('%B-%Y')
        current_date = frappe.utils.add_months(current_date, months=1)
        
        columns.append({

                "label": month,
                "fieldtype": "Float",
                "fieldname": frappe.scrub(month),
                "print_width": 10
            })
    columns+=[
        {
            "label": _("Employee Base Details"),
            "fieldtype": "Data",
            "fieldname": "base_months",
            "width": 100
        },
        {
            "label": _("Total Working Days"),
            "fieldtype": "Float",
            "fieldname": "working_days",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldtype": "Float",
            "fieldname": "total_salary_amount",
            "width": 100
        },
        {
            "label": _("Total Bonus Amount"),
            "fieldtype": "Float",
            "fieldname": "total_bonus_amount",
            "width": 100
        },

    ]
    return columns

def get_data(filters):
    keys = list(filters.keys())
    no=0
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    settings = frappe.get_single("United Knitting Mills Settings")
    emp_filter = {'from_date':["=", filters['from_date']],"to_date":["=", filters['to_date']],'docstatus': ["!=", 2], 'unit':filters['unit']}
    if ("department" in keys):
        emp_filter["department"] = filters["department"]
    else:
        emp_filter["department"] = ["in", frappe.db.get_all("Department", filters={"is_staff":0}, pluck="name")]
    if ("designation" in keys):
        emp_filter["designation"] = filters["designation"]
    bonus_list=frappe.db.get_all("Employee Bonus", filters=emp_filter, fields=["name","employee","employee_name", "working_days", "bonus_amount", "designation", "total_salary_amount", "from_date", "to_date", "total_bonus_amount"],group_by="employee", order_by="employee")
    for bonus in bonus_list:
        emp_doc = frappe.get_doc("Employee", bonus.employee)
        attendance_monthwise=frappe.db.sql(f'''
                    SELECT 
                    (SELECT dep.is_staff FROM `tabDepartment` dep WHERE dep.name = att.department limit 1) as is_staff,
                        count(att.name) as days, monthname(att.attendance_date) as month, year(att.attendance_date) as year,
                        (SELECT  esd.base 
                        FROM `tabEmployee Salary Details` esd
                        WHERE ((att.attendance_date >= esd.from_date and ifnull(esd.to_date, "")='') or (att.attendance_date between esd.from_date and esd.to_date)) and esd.workflow_state = 'Approved by MD' and 
                        esd.docstatus = 1 and esd.employee=att.employee limit 1) as base
                    FROM `tabAttendance` as att
                    WHERE  
                        att.employee = '{bonus['employee']}' and 
                        att.attendance_date between GREATEST('{from_date}', '{bonus['from_date']}') and LEAST('{to_date}', '{bonus['to_date']}') and 
                        att.total_shift_count >= 1 and DATE_FORMAT(att.attendance_date, '%W') != 'Sunday' and
                        (SELECT dep.is_staff FROM `tabDepartment` dep WHERE dep.name = att.department limit 1) = 0 and
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
                        att.docstatus = 1 and 
                         (SELECT  count(esd.name) 
                        FROM `tabEmployee Salary Details` esd
                        WHERE ((att.attendance_date >= esd.from_date and ifnull(esd.to_date, "")='') or (att.attendance_date between esd.from_date and esd.to_date)) and esd.workflow_state = 'Approved by MD' and 
                        esd.docstatus = 1 and esd.employee=att.employee limit 1) >0
                    GROUP BY monthname(att.attendance_date), year(att.attendance_date), 
                    (SELECT  esd.name
                        FROM `tabEmployee Salary Details` esd
                        WHERE ((att.attendance_date >= esd.from_date and ifnull(esd.to_date, "")='') or (att.attendance_date between esd.from_date and esd.to_date)) and esd.workflow_state = 'Approved by MD' and 
                        esd.docstatus = 1 and esd.employee=att.employee limit 1)
                                           ''', as_dict=1)
        _months=[
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
        ]
        attendance_monthwise.sort(key=lambda x : (x.get('year'),_months.index(x.get('month'))))
        base = {}
        no+=1
        for att in attendance_monthwise:
            if att.base not in base:
                base[att.base] = []
            base[att.base].append(f"{att.month}-{att.year}")
            bonus[frappe.scrub(f"{att.month}-{att.year}")] = att.days
        bonus['base_months'] = "<br>".join([f"""{month} - {', '.join(base[month])}""" for month in base])
        bonus['status'] = emp_doc.status
        bonus['current_wages']=frappe.db.get_value("Salary Structure Assignment", {'employee':bonus.employee, 'docstatus':1, 'workflow_state':"Approved by MD"}, 'base')
        bonus['sno']=str(no)
    return bonus_list