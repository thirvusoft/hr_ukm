// Copyright (c) 2023, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Commision Details Report"] = {
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
				"fieldname": "employee",
				"label": __("Commsion Employee"),
				"fieldtype": "Link",
				"options": "Employee",
				"width": "80",
				"get_query": function() {
					return {
						"query": "united_knitting_mills.ukm.report.employee_commision_details_report.employee_commision_details_report.employement_list",
					}
				}
			}

	]
};
