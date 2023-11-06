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
        {
            "label": _("Total Working Days"),
            "fieldtype": "Float",
            "fieldname": "working_days",
            "width": 100
        },
        {
            "label": _("Total Salary Amount"),
            "fieldtype": "Currency",
            "fieldname": "total_salary_amount",
            "width": 100
        },
      
         {
            "label": _("Bonus %"),
            "fieldtype": "Float",
            "fieldname": "bonus_percentage",
            "width": 100
        },
         
    	{
            "label": _("Bonus Amount"),
            "fieldtype": "Currency",
            "fieldname": "total_bonus_amount",
            "width": 100
        },
     	{
            "label": _("Leave Days"),
            "fieldtype": "Float",
            "fieldname": "leave_days",
            "width": 100
        },
     	{
            "label": _("Leave Salary"),
            "fieldtype": "Currency",
            "fieldname": "leave_salary",
            "width": 100
        },
	     	{
            "label": _("Settlement Days"),
            "fieldtype": "Float",
            "fieldname": "settlement_days",
            "width": 100
        },
     	{
            "label": _("Settlement Salary"),
            "fieldtype": "Currency",
            "fieldname": "settlement_salary",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "fieldname": "bonus_amount",
            "width": 100
        },

    ]
    return columns

def get_data(filters):
    keys = list(filters.keys())
    no=0
    filter = {'from_date':["=", filters['from_date']],"to_date":["=", filters['to_date']],'docstatus': ["!=", 2], 'unit':filters['unit']}
    
    if ("department" in keys):
        filter["department"] = filters["department"]
        
    if ("designation" in keys):
        filter["designation"] = filters["designation"]

    bonus_list=frappe.db.get_all("Employee Bonus", filters=filter, fields=["name","employee","employee_name","designation", "working_days", "bonus_amount","bonus_percentage",  
                                "settlement_days", "settlement_salary", "leave_days", "leave_salary", "total_salary_amount", "total_bonus_amount"],
                                group_by="employee", order_by="employee")
    
    for bonus in bonus_list:
        no+=1
        emp_doc = frappe.get_doc("Employee", bonus.employee)
        bonus['status'] = emp_doc.status
        bonus['current_wages']=frappe.db.get_value("Salary Structure Assignment", {'employee':bonus.employee, 'docstatus':1, 'workflow_state':"Approved by MD"}, 'base')
        bonus['sno']=str(no)
    return bonus_list