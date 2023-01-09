# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe

from erpnext.education.report.student_monthly_attendance_sheet.student_monthly_attendance_sheet import daterange
from frappe import _

from datetime import date

def execute(filters = None):

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	start_date = tuple(map(int, from_date.split('-')))
	end_date = tuple(map(int, to_date.split('-')))

	between_dates = list(map(str, list(daterange(date(start_date[0], start_date[1], start_date[2]),date(end_date[0], end_date[1], end_date[2])))))
	
	columns = get_columns(between_dates)

	doc_filters = {'from_date': ["between", (from_date, to_date)], "to_date": ["between",(from_date, to_date)], 'docstatus':['!=', 2] }
	
	if filters.get("designation"):
		doc_filters["designation"] = filters.get("designation")

	if filters.get("department"):
		doc_filters["department"] = filters.get("department")

	if filters.get("unit"):
		doc_filters["unit"] = filters.get("unit")
	if filters.get("status"):
		if filters.get("status")=="Yes":
				doc_filters["is_hold"] = 1
				
		elif filters.get("status")=="No" :
				doc_filters["is_hold"] = 0

	data = get_data(from_date, to_date, between_dates, doc_filters)

	return columns, data


def get_columns(between_dates):

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
			"label": _("Account Number"),
			"fieldtype": "Data",
			"fieldname": "account_number",
			"width": 150
		},
		{
			"label": _("IFSC"),
			"fieldtype": "Data",
			"fieldname": "ifsc",
			"width": 100
		},
		{
			"label": _("Bank"),
			"fieldtype": "Data",
			"fieldname": "bank",
			"width": 100
		},
		{
			"label": _("Branch Name"),
			"fieldtype": "Data",
			"fieldname": "branch_name",
			"width": 120
		},
		{
			"label": _("Mode"),
			"fieldtype": "Data",
			"fieldname": "mode",
			"width": 80
		},
		{
			"label": _("Salary"),
			"fieldtype": "Currency",
			"fieldname": "salary",
			"width": 80
		}
	]

	for i in between_dates:

		columns.append(
			{
				"label": i[len(i)-2:],
				"fieldtype": "Float",
				"fieldname": i,
				"print_width": 10
			}
		)

	columns += [
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
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 80
        },
		{
			"label": _("Total Advance"),
			"fieldtype": "Currency",
			"fieldname": "total_advance",
			"width": 100
		},
		{
			"label": _("Signature"),
			"fieldtype": "Data",
			"fieldname": "signature",
			"width": 200
		}
	]

	return columns

def get_data(from_date, to_date, between_dates, doc_filters):

	data = []

	emp_advance_list = frappe.db.get_all("Employee Advance", 
	 	filters = doc_filters, 
		fields = ["name", "employee", "employee_name", "total_shift", "eligible_amount", "advance_amount", "designation","is_hold"],		
		order_by = "designation"
	)
	no=1
	non_hold=0
	for emp_advance in emp_advance_list:

		sub_data = frappe._dict()

		emp_doc = frappe.get_doc("Employee",emp_advance.employee)

		salary_structure_assignment_base = frappe.db.get_value("Salary Structure Assignment", {'employee':emp_advance.employee, 'docstatus':1}, 'base')
		
		if emp_advance["is_hold"]:
			hold = "Hold"
			non_hold=non_hold+emp_advance["advance_amount"]
		else:
			hold = ""
		sub_data.update(
			{	"sno":str(no),
				"designation" : emp_advance.designation,
				"code" : emp_advance.employee,
				"worker_name":emp_advance.employee_name,
				"account_number" : emp_doc.bank_ac_no,
				"ifsc" : emp_doc.ifsc_code,
				"bank" : emp_doc.bank_name,
				"branch_name" : emp_doc.ts_bank_branch_name,
				"mode" : emp_doc.salary_mode,
				"salary": salary_structure_assignment_base
			}
		)

		for date in between_dates:
			get_attendance = frappe.db.get_value("Attendance", {'employee':emp_advance.employee, 'docstatus':1, 'attendance_date':date}, 'total_shift_count')
			
			sub_data.update(
				{
					date: get_attendance
				}
			)

		sub_data.update(
				{
					"total_shift": emp_advance.total_shift,
					"total_amount": emp_advance.eligible_amount,
					"status":hold,
					"total_advance": emp_advance.advance_amount,
					"signature": None
					
				}
			)

		data.append(sub_data)
		no+=1


	

	# designation_check =''

	# for i in range (0,len(data),1):
	# 	if data[i][0] != designation_check:
	# 		designation_check = data[i][0] 
	# 		data[i][0] = f'<b>{data[i][0]}</b>'
		   
	# 	else:
	# 		data[i][0]=''
	
	if data:
		data.append({"status":"Total Hold Amount","total_advance":non_hold})
	# data = [list(i.values()) for i in data]
	
	return data
