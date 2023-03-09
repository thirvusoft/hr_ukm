// Copyright (c) 2023, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Costing Report"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":  frappe.datetime.nowdate(),
			"width": "80",
			"reqd": 1
		},
		{
			"fieldname":"unit",
			"label": __("Unit"),
			"fieldtype": "Link",
			"options": "Location",
			"width": "100",
			"reqd":1
		},
		{
			"fieldname":"designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": "100",
			"get_query": function () {
				var unit = frappe.query_report.get_filter_value('unit');
				return {
					filters: [
						["Designation", "unit", "=", unit]
					]
				};
			},
		}
	]
};
