# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt
from ctypes.wintypes import PFLOAT
import frappe
import pandas
from datetime import date, datetime, timedelta
from frappe import _
from erpnext.education.report.student_monthly_attendance_sheet.student_monthly_attendance_sheet import daterange



def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
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
			"fieldtype": "Link",
			"fieldname": "designation",
			"options":"Designation",
			"width": 100
		},
		{
			"label": _("Sourced"),
			"fieldtype": "Employee",
			"fieldname": "source_employee",
			"options":"Employee",
			"width": 100
		},
		{
			"label": _("Current Salary"),
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
		columns+=[{

			"label": i[len(i)-2:],
			"fieldtype": "Float",
			"fieldname": i,
			"print_width": 10
		},]
	columns+=[
	{
		"label": _("Total Shift"),
		"fieldtype": "Float",
		"fieldname": "total_shift",
		"width": 100
	},
	{
		"label": _("Amount"),
		"fieldtype": "Currency",
		"fieldname": "commision_amount",
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
	data_list = []
	from_date = filters["from_date"]
	to_date = filters["to_date"]
	no=0
	ukm_settings=frappe.db.get_single_value('United Knitting Mills Settings', 'employment_type_for_commision_calculation')
	if ukm_settings:
		commision_filter={"status":"Active", "employment_type":ukm_settings}
		if filters.get("employee"):
			commision_filter["name"] = filters.get("employee")
		commision_employee = frappe.db.get_all("Employee", filters=commision_filter, fields=["name","employee_name"])
		for employee in commision_employee:
			comission_amount=frappe.get_doc("Employee", employee.name)
			for amt in comission_amount.employee_commision:
				if amt.gender == "Male":
					amount_m = amt.commision_amount or 0
				if amt.gender == "Female":
					amount_f = amt.commision_amount or 0
			contract_employee = frappe.db.get_all("Employee", filters={"status":"Active", "employment_type": "Contract", "commision_agent":employee.name}, fields=["name", "employee_name","commision_agent", "gender", "designation"])
			for contract in contract_employee:
				no+=1
				get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':contract.name, 'docstatus':1}, 'base')
				data={}
				data["sno"] = str(no)
				data["code"]=contract.name
				data["worker_name"]=contract.employee_name
				data["designation"]=contract.designation
				data["salary"]=get_ssa or 0
				data["source_employee"]=employee.employee_name
				if contract.gender == "Female":
					data["commision_amount"] = amount_f
				if contract.gender == "Male":
					data["commision_amount"] = amount_m
				get_attendance=frappe.get_all("Attendance", filters={'employee':contract.name, 'workflow_state':"Present",'attendance_date':["between", [from_date, to_date]]}, fields=['total_shift_count', 'name'])
				total_shift = 0
				for i in get_attendance:
					att_date=frappe.db.get_value("Attendance", i.name, "attendance_date")
					if i.total_shift_count >=1.50:
						i.total_shift_count =1.50
					data[str(att_date)]=i.total_shift_count
					total_shift += i.total_shift_count
				data["total_shift"] = total_shift
				if contract.gender == "Female":
					data["total_amount"] = total_shift *amount_f
				if contract.gender == "Male":
					data["total_amount"] = total_shift *amount_m
				data_list.append(data)
	return data_list

@frappe.whitelist()
def employement_list(doctype, txt, searchfield, start, page_len, filters):
	ukm_settings=frappe.db.get_single_value('United Knitting Mills Settings', 'employment_type_for_commision_calculation')
	if txt:
		return frappe.db.sql(f'''select name, employee_name from `tabEmployee` where employment_type = '{ukm_settings}' and (name like '%{txt}%' or employee_name like '%{txt}%') ''')
	else:
		return frappe.db.sql(f'''select name, employee_name from `tabEmployee` where employment_type = '{ukm_settings}' ''')
     