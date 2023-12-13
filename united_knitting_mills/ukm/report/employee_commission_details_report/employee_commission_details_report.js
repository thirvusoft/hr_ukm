// Copyright (c) 2023, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Commission Details Report"] = {
	"filters": [
			{
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"reqd": 1,
				"width": "80"
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"reqd": 1,
				"width": "80"
			},
			{
				"fieldname": "unit",
				"label": __("Unit"),
				"fieldtype": "Link",
				"options": "Location",
				"width": "100",
				"reqd": 1
			},
			{
				"fieldname": "department",
				"label": __("Department"),
				"fieldtype": "Link",
				"options": "Department",
				"width": "100",
				"get_query": function () {
					var unit = frappe.query_report.get_filter_value('unit');
					return {
						filters: [
							["Department", "unit", "=", unit]
						]
					};
				},
			},
			{
				"fieldname": "employee",
				"label": __("Commission Employee"),
				"fieldtype": "Link",
				"options": "Employee",
				"width": "80",
				"get_query": function() {
					return {
						"query": "united_knitting_mills.ukm.report.employee_commission_details_report.employee_commission_details_report.employement_list",
					}
				}
			}
	]
};
