# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
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
            "label": _("Status"),
            "fieldtype": "Select",
            "fieldname": "status",
            "options":["", "Active", "Inactive", "Suspended", "Left"]
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
            "fieldname": "total_working_days",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldtype": "Float",
            "fieldname": "total_amount",
            "width": 100
        },

    ]
    return columns

def get_data(filters):
    data=[]

    filter = {'from_date':["=", filters['from_date']],"to_date":["=", filters['to_date']],'docstatus': ["!=", 2], 'unit':filters['unit']}
    bonus_list=frappe.db.get_all("Employee Bonus", filters=filter, fields=["name","employee","employee_name", "working_days", "bonus_amount"],group_by="employee", order_by="employee")
    for bonus in bonus_list:
        emp_doc = frappe.get_doc("Employee",bonus.employee)
        get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':j.employee, 'docstatus':1, 'workflow_status':"Approved by MD"}, 'base')
        
