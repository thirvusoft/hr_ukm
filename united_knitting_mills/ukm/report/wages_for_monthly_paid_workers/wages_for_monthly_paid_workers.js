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
		{
			"fieldname":"location",
			"label": __("Location"),
			"fieldtype": "Link",
			"options": "Location",
			"width": "100",
			on_change:function(){
				frappe.db.get_value('Location', frappe.query_report.get_filter_value('location'), 'address', function(value) {
					if (value['address']){

						frappe.model.with_doc("Address", value['address'], function(r) {
							var add = frappe.model.get_doc("Address", value['address']);
							var str = add.address_line1
	
							if(add.address_line2){
								str += " "+add.address_line2+ "," + add.city
							}else{
								str += "," + add.city
							}
							if (add.pincode){
								str += "-" +add.pincode
							}
							if(add.state){
								str +=","+ add.state
							}
							frappe.query_report.set_filter_value('address',str)					}
						)
					}
					else{
						frappe.query_report.set_filter_value('address','')					

					}
			})
		}
		},
		{
			"fieldname":"address",
			"label": __("Address"),
			"fieldtype": "Small Text",
			"hidden":0,
			"width": "100"
		},
	],
	onload:function(frm){
		frappe.db.get_value('Employee', {'user_id':frappe.session.user}, ['location','name'], function(data) {
			var location=data.location
			if (location){
				frappe.query_report.set_filter_value("location",location);
			}
		})
	}
 };

