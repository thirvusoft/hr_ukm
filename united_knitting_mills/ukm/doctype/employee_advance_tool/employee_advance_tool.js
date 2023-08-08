frappe.ui.form.on("Employee Advance Tool",{
	get_employees:function(frm,cdt,cdn){

		frm.set_value("total_advance_amount",0)

		frm.clear_table("employee_advance_details");
		cur_frm.refresh_field("employee_advance_details")

		var advance = locals[cdt][cdn]

		var designation = advance.designation
		var department = advance.department
		var location = advance.ts_location
		var from_date = advance.from_date
		var to_date = advance.to_date

		frappe.call({
			method: "united_knitting_mills.ukm.doctype.employee_advance_tool.employee_advance_tool.employee_finder",
			args:{location, from_date, to_date, designation, department},
			
			callback(r){

				for(let i = 0; i < r.message[0].length; i++){
					var child = cur_frm.add_child("employee_advance_details");

					frappe.model.set_value(child.doctype, child.name, "employee", r.message[0][i]["name"])
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[0][i]["employee_name"])
					frappe.model.set_value(child.doctype, child.name, "designation", r.message[0][i]["designation"])
					frappe.model.set_value(child.doctype, child.name, "payment_method", 'Deduct from Salary')
					frappe.model.set_value(child.doctype, child.name, "eligible_amount", r.message[0][i]["eligible_amount"] || 0)
					frappe.model.set_value(child.doctype, child.name, "current_advance", r.message[0][i]["current_advance"] || 0)
					frappe.model.set_value(child.doctype, child.name, "total_shift", r.message[0][i]["total_shift"] || 0)
					frappe.model.set_value(child.doctype, child.name, "department", r.message[0][i]["department"] || 0)

				}
				cur_frm.refresh_field("employee_advance_details")

				frm.set_value("total_advance_amount",r.message[1])
			}
		})
	},
})
