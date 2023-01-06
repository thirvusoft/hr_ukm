// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Details Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd":1,
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd":1,
			"width": "80"
		},
		{
			"fieldname":"staff_labour",
			"label": __("Staff / Labour"),
			"fieldtype": "Select",
			"options": "Staff\nLabour",
			"width": "100",
			"reqd":1
		},
		{
			"fieldname":"status",
			"label": __("Is Hold"),
			"fieldtype": "Select",
			"options": "\nYes\nNo",
			"width": "100"
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
		{
			"fieldname":"unit",
			"label": __("Unit"),
			"fieldtype": "Link",
			"options": "Location",
			"width": "100"
		},
	]
};
