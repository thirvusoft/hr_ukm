// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt
	
frappe.ui.form.on("Employee Bonus Tool",{
	from_date:function(frm){
		frm.set_value("emp_department","")
	},
	to_date:function(frm){
		frm.set_value("emp_department","")
	},
	location:function(frm){
		frm.set_value("emp_department","")
	},
	emp_department:function(frm){
		var emp_department=frm.doc.emp_department
		if (emp_department){
			var from_date=frm.doc.from_date
			var to_date = frm.doc.to_date	
			var location = frm.doc.location
			frappe.call({
				method:"united_knitting_mills.ukm.doctype.employee_bonus_tool.employee_bonus_tool.employee_finder",
				args:{emp_department,location,from_date,to_date},
				callback(r){
					frm.set_value('employee_bonus_details', r.message[3])
					// frm.clear_table("employee_bonus_details");
					// frm.set_value("total_bonus_amount",0)
					// for(var i=0;i<r.message[0].length;i++){
					// 	var child = cur_frm.add_child("employee_bonus_details");
					// 	frappe.model.set_value(child.doctype, child.name, "employee", r.message[0][i]["name"])
					// 	frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[0][i]["employee_name"])
					// 	frappe.model.set_value(child.doctype, child.name, "designation", designation)
					// 	frappe.model.set_value(child.doctype, child.name, "working_days", r.message[2][i])
					// 	frappe.model.set_value(child.doctype, child.name, "current_bonus", r.message[1][i])
					// }
					cur_frm.refresh_field("employee_bonus_details")
				}
			})
		}
		else{
			frm.clear_table("employee_bonus_details");
			cur_frm.refresh_field("employee_bonus_details")
			frm.set_value("total_bonus_amount",0)
		}

	}
});
	 
