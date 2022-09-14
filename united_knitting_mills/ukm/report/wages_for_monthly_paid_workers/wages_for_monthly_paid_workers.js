// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Wages for Monthly Paid Workers"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"width": "80",
			
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.month_end(),
			"width": "80",
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