# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from dateutil.relativedelta import relativedelta
from frappe.utils.data import nowdate

from frappe.utils import (
	date_diff,
	getdate,
)

from erpnext.hr.utils import get_holiday_dates_for_employee

def execute(filters=None):

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():

	columns = [

		{
			"label": _("Designation"),
			"fieldtype": "Link",
			"options":"Designation",
			"fieldname": "designation",
			"width": 170
		},

		{
			"label": _("Total Employee Count"),
			"fieldtype": "Int",
			"fieldname": "total_employee_count",
			"width": 170
		},

		{
			"label": _("Present Employee Count"),
			"fieldtype": "Int",
			"fieldname": "present_employee_count",
			"width": 180
		},

		{
			"label": _("Absent Employee Count"),
			"fieldtype": "Int",
			"fieldname": "absent_employee_count",
			"width": 180
		},

		{
			"label": _("Wages -> (0.25 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_0_25_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (0.50 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_0_50_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (0.75 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_0_75_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (1 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_1_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (1.25 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_1_25_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (1.50 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_1_50_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (1.75 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_1_75_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (2 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_2_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (2.25 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_2_25_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (2.50 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_2_50_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (2.75 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_2_75_shift",
			"width": 160
		},

		{
			"label": _("Wages -> (3 Shift)"),
			"fieldtype": "Currency",
			"fieldname": "wages_3_shift",
			"width": 160
		},

	]

	return columns

def get_data(filters):

	data = []
	filters_des = {}
	if filters.get('unit'):
			filters_des.update({
				'unit':filters.get('unit')
			})
	if filters.get("designation"):
		filters_des.update({"name": filters.get("designation")})
		
		designation_list = frappe.get_all("Designation", filters_des, ["name", "thirvu_shift"], order_by = "name" )

	else:
		designation_list = frappe.get_all("Designation", filters_des,["name", "thirvu_shift"], order_by = "name" )

	
	for designation in designation_list:

		filters_emp = {"designation": designation["name"], "status": "Active"}
		if filters.get('unit'):
			filters_emp.update({
				'location':filters.get('unit')
			})
			
		sub_data = frappe._dict()

		present_count = 0

		wages = 0

		emp_list = frappe.get_all("Employee",filters_emp, ["name"])

		filtered_date = getdate(filters.get("date"))

		employee_type = frappe.get_value("Employee Timing Details", {"name": designation["thirvu_shift"]}, "staff")


		if filters.get("date") == str(nowdate()):

			if employee_type:

				for emp in emp_list:

					if frappe.get_all("Employee Checkin Without Log Type", filters = {"employee": emp["name"], "time": ["between", (filtered_date, filtered_date)]}, fields = ["name"]):
						present_count = present_count + 1

						wage = frappe.get_value("Salary Structure Assignment", {"employee": emp["name"], "docstatus": 1}, "base")

						last_date_of_month = getdate(filtered_date) + relativedelta(day=1, months=+1, days=-1)
						first_date_of_month = getdate(filtered_date) + relativedelta(day=1)

						payment_days = date_diff(last_date_of_month, first_date_of_month) + 1

						holidays = get_holiday_dates_for_employee(emp["name"], first_date_of_month, last_date_of_month)
						payment_days -= len(holidays)

						if wage:
							wages = wages + wage / payment_days

				sub_data.update(

					{   
						"designation": designation["name"],
						"total_employee_count": len(emp_list),
						"present_employee_count": present_count,
						"absent_employee_count": len(emp_list) - present_count,
						"wages_0_25_shift": 0,
						"wages_0_50_shift": wages * 0.50,
						"wages_0_75_shift": 0,
						"wages_1_shift": wages,
						"wages_1_25_shift": 0,
						"wages_1_50_shift": 0,
						"wages_1_75_shift": 0,
						"wages_2_shift": 0,
						"wages_2_25_shift": 0,
						"wages_2_50_shift": 0,
						"wages_2_75_shift": 0,
						"wages_3_shift": 0
					}

				)

				data.append(sub_data)
					
			else:

				for emp in emp_list:

					if frappe.get_all("Employee Checkin Without Log Type", filters = {"employee": emp["name"], "time": ["between", (filtered_date, filtered_date)]}, fields = ["name"]):
						present_count = present_count + 1

						wage = frappe.get_value("Salary Structure Assignment", {"employee": emp["name"], "docstatus": 1}, "base")

						if wage:
							wages = wages + wage

				sub_data.update(

					{   
						"designation": designation["name"],
						"total_employee_count": len(emp_list),
						"present_employee_count": present_count,
						"absent_employee_count": len(emp_list) - present_count,
						"wages_0_25_shift": wages * 0.25,
						"wages_0_50_shift": wages * 0.50,
						"wages_0_75_shift": wages * 0.75,
						"wages_1_shift": wages,
						"wages_1_25_shift": wages * 1.25,
						"wages_1_50_shift": wages * 1.50,
						"wages_1_75_shift": wages * 1.75,
						"wages_2_shift": wages * 2,
						"wages_2_25_shift": wages * 2.25,
						"wages_2_50_shift": wages * 2.50,
						"wages_2_75_shift": wages * 2.75,
						"wages_3_shift": wages * 3
					}

				)

				data.append(sub_data)

		else:

			if employee_type:

				wages_0_50_shift = 0
				wages_1_shift = 0

				for emp in emp_list:

					attendance_list = frappe.get_all("Attendance", filters = {"employee": emp["name"], "docstatus": 1, "attendance_date": ["between", (filtered_date, filtered_date)]}, fields = ["total_shift_count"])
					
					if attendance_list:

						present_count = present_count + 1

						wage = frappe.get_value("Salary Structure Assignment", {"employee": emp["name"], "docstatus": 1}, "base")

						if wage:
							last_date_of_month = getdate(filtered_date) + relativedelta(day=1, months=+1, days=-1)
							first_date_of_month = getdate(filtered_date) + relativedelta(day=1)

							payment_days = date_diff(last_date_of_month, first_date_of_month) + 1

							holidays = get_holiday_dates_for_employee(emp["name"], first_date_of_month, last_date_of_month)
							payment_days -= len(holidays)

							if attendance_list[0]["total_shift_count"] == 0.50:
								wages_0_50_shift += (wage / payment_days) * 0.50

							elif attendance_list[0]["total_shift_count"] == 1:
								wages_1_shift += wage / payment_days

				sub_data.update(

					{   
						"designation": designation["name"],
						"total_employee_count": len(emp_list),
						"present_employee_count": present_count,
						"absent_employee_count": len(emp_list) - present_count,
						"wages_0_25_shift": 0,
						"wages_0_50_shift": wages_0_50_shift,
						"wages_0_75_shift": 0,
						"wages_1_shift": wages_1_shift,
						"wages_1_25_shift": 0,
						"wages_1_50_shift": 0,
						"wages_1_75_shift": 0,
						"wages_2_shift": 0,
						"wages_2_25_shift": 0,
						"wages_2_50_shift": 0,
						"wages_2_75_shift": 0,
						"wages_3_shift": 0
					}

				)

				data.append(sub_data)
					
			else:

				wages_0_25_shift = 0
				wages_0_50_shift = 0
				wages_0_75_shift = 0
				wages_1_shift = 0
				wages_1_25_shift = 0
				wages_1_50_shift = 0
				wages_1_75_shift = 0
				wages_2_shift = 0
				wages_2_25_shift = 0
				wages_2_50_shift = 0
				wages_2_75_shift = 0
				wages_3_shift = 0

				for emp in emp_list:

					attendance_list = frappe.get_all("Attendance", filters = {"employee": emp["name"], "docstatus": 1, "attendance_date": ["between", (filtered_date, filtered_date)]}, fields = ["total_shift_count", "total_shift_amount"])

					if attendance_list:

						present_count = present_count + 1

						if attendance_list[0]["total_shift_count"] == 0.25:
							wages_0_25_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 0.50:
							wages_0_50_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 0.75:
							wages_0_75_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 1:
							wages_1_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 1.25:
							wages_1_25_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 1.5:
							wages_1_50_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 1.75:
							wages_1_75_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 2:
							wages_2_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 2.25:
							wages_2_25_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 2.5:
							wages_2_50_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 2.75:
							wages_2_75_shift += attendance_list[0]["total_shift_amount"]

						elif attendance_list[0]["total_shift_count"] == 3:
							wages_3_shift += attendance_list[0]["total_shift_amount"]

				sub_data.update(

					{   
						"designation": designation["name"],
						"total_employee_count": len(emp_list),
						"present_employee_count": present_count,
						"absent_employee_count": len(emp_list) - present_count,
						"wages_0_25_shift": wages_0_25_shift,
						"wages_0_50_shift": wages_0_50_shift,
						"wages_0_75_shift": wages_0_75_shift,
						"wages_1_shift": wages_1_shift,
						"wages_1_25_shift": wages_1_25_shift,
						"wages_1_50_shift": wages_1_50_shift,
						"wages_1_75_shift": wages_1_75_shift,
						"wages_2_shift": wages_2_shift,
						"wages_2_25_shift": wages_2_25_shift,
						"wages_2_50_shift": wages_2_50_shift,
						"wages_2_75_shift": wages_2_75_shift,
						"wages_3_shift":wages_3_shift
					}

				)

				data.append(sub_data)

	return data
