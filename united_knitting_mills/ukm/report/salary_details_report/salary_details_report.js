// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Details Report"] = {
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
			"fieldname": "staff_labour",
			"label": __("Staff / Labour"),
			"fieldtype": "Select",
			"options": "Staff\nLabour",
			"width": "100",
			"reqd": 1
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
			"fieldname": "status",
			"label": __("Is Hold"),
			"fieldtype": "Select",
			"options": "\nYes\nNo",
			"width": "100"
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
			"fieldname": "designation",
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
		},
		{
			"fieldname":"holding_transition",
			"label": __("Hold Slip Verified "),
			"fieldtype": "Check",
			"width": "100"
		},
	]
};
frappe.realtime.on('refresh-report', () => {
	var a = document.getElementsByClassName('dt-cell')
	console.log(a)
	Array.from(a).forEach((d) => {
		console.log(d.innerText)
		if (d.innerText == 'Total Hold Amount') {
			console.log('ineer')
			debugger
			d.style.color = 'red'
			d.style.fontWeight = 'bold'
		}
	})
})

$(document).ready(() => {
	setTimeout(() => {
		if (["poojaukm1@hr.ukm", "rajasekarm@gmail.com"].includes(frappe.session.user)) {
			document.querySelector(`ul.dropdown-menu.dropdown-menu-right li span[data-label="Export"]`).parentElement.parentElement.remove()
		}
	}, 1000)

});