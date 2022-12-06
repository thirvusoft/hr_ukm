// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */
 
frappe.query_reports["Daily Attendance Report"] = {
	"filters": [
		{
			"fieldname":"attendance_date",
			"label": __("Attendance Date"),
			"fieldtype": "Date",
			"default":  frappe.datetime.add_days(frappe.datetime.nowdate(),-1),
			"width": "80"
		},
		{
			"fieldname":"designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": "100"
		},
		{
			"fieldname":"staff_or_labour",
			"label": __("Staff / Labour"),
			"fieldtype": "Select",
			"options": "\nStaff\nLabour",
			"width": "100"
		},
	]
 };
 