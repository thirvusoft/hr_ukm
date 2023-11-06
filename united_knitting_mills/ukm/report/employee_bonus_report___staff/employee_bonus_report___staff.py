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

				"label": f'{month} - Days',
				"fieldtype": "Float",
				"fieldname": f'{frappe.scrub(month)}-days',
				"print_width": 10
			})
		
		columns.append({

				"label":f'{month} - Salary' ,
				"fieldtype": "Float",
				"fieldname": f'{frappe.scrub(month)}-salary',
				"print_width": 10
			})
	columns+=[
		{
			"label": _("Total Working Days"),
			"fieldtype": "Float",
			"fieldname": "working_days",
			"width": 100
		},
		{
			"label": _("Total Salary"),
			"fieldtype": "Float",
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
	filter = {'from_date':["=", filters['from_date']],"to_date":["=", filters['to_date']],'docstatus': ["!=", 2], 'unit':filters['unit']}
	if ("department" in keys):
		filter["department"] = filters["department"]
	if ("designation" in keys):
		filter["designation"] = filters["designation"]
	bonus_list=frappe.db.get_all("Employee Bonus", filters=filter, fields=["unit","name","employee","employee_name", "working_days", "bonus_amount", "designation", "total_salary_amount", "from_date", "to_date", "total_bonus_amount", "bonus_percentage"],group_by="employee", order_by="employee")
	for bonus in bonus_list:
		emp_doc = frappe.get_doc("Employee", bonus.employee)
		employee_bonus = frappe.db.sql(f""" 
				SELECT
					ss.total_working_days,
					sum(ss.payment_days) as payment_days,
					ss.absent_days,
					ss.leave_with_pay,
					sum(ss.gross_pay) as gross_pay,
					monthname(ss.start_date) as month, year(ss.start_date) as year
				FROM `tabSalary Slip` ss
				WHERE
					ss.employee = '{bonus['employee']}' AND
					ss.docstatus = 1 AND
					ss.unit = '{bonus['unit']}' AND
					ss.start_date between '{from_date}' AND '{to_date}' and
					ss.end_date between '{from_date}' AND '{to_date}'
				GROUP BY
					monthname(ss.start_date), year(ss.start_date)
				ORDER BY
					ss.employee, monthname(ss.start_date), year(ss.start_date)
				
					""", as_dict=1) 
		for row in employee_bonus:
			bonus[f'{frappe.scrub(row["month"])}_{frappe.scrub(str(row["year"]))}-days'] = row["payment_days"]
			bonus[f'{frappe.scrub(row["month"])}_{frappe.scrub(str(row["year"]))}-salary'] = row["gross_pay"]
		no+=1
		bonus['status'] = emp_doc.status
		bonus['current_wages']=frappe.db.get_value("Salary Structure Assignment", {'employee':bonus.employee, 'docstatus':1, 'workflow_state':"Approved by MD"}, 'base')
		bonus['sno']=str(no)
		months=[
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
	return bonus_list
