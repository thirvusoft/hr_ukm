// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Checkin Report"] = {
	"filters": [
		{
			"fieldname":"attendance_date",
			"label": __("Attendance Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": "100"
		},
		{
			"fieldname":"designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": "100"
		},
	]
 };