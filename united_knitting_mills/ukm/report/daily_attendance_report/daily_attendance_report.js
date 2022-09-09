// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */
 
frappe.query_reports["Daily Attendance Report"] = {
	"filters": [
		{
			"fieldname":"attendance_date",
			"label": __("Attendance Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80"
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
 