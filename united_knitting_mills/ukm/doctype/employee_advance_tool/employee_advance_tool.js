	
frappe.ui.form.on("Employee Advance Tool",{
	get_employees:function(frm,cdt,cdn){
		var advance=locals[cdt][cdn]
		var designation = advance.designation
		var department = advance.department
		var location = advance.ts_location
		if(location){
			
			frappe.call({
				method:"united_knitting_mills.ukm.doctype.employee_advance_tool.employee_advance_tool.employee_finder",
				args:{designation,location,department},
				callback(r){
					frm.clear_table("employee_advance_details");
					for(let i=0;i<r.message.length;i++){
						var child = cur_frm.add_child("employee_advance_details");
						frappe.model.set_value(child.doctype, child.name, "employee", r.message[i]["name"])
						frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i]["employee_name"])
						frappe.model.set_value(child.doctype, child.name, "designation", r.message[i]["designation"])
						frappe.model.set_value(child.doctype, child.name, "payment_method",'Deduct from Salary')
						frappe.model.set_value(child.doctype, child.name, "eligible_amount",r.message[i]["eligible_amount"] || 0)
						frappe.model.set_value(child.doctype, child.name, "current_advance",r.message[i]["current_advance"] || 0)

					}
					cur_frm.refresh_field("employee_advance_details")
				}
			})
		}
		else{
			frappe.msgprint('Location not assigned for this user')
		}	
	},
	
	on_submit:function(frm,cdt,cdn){
		var advance=locals[cdt][cdn]
		for(let i=0;i<advance.employee_advance_details.length;i++){
			frappe.call({
				method:"united_knitting_mills.ukm.doctype.employee_advance_tool.employee_advance_tool.create_employee_advance",
				args:{amount:advance.employee_advance_details[i].current_advance,
					eligible_amount:advance.employee_advance_details[i].eligible_amount,
					name:advance.employee_advance_details[i].employee,
					date:frm.doc.date,
					payment_type:advance.employee_advance_details[i].payment_method},
			})
		}
	},
	before_save:function(frm, cdt, cdn) {

		var table = frm.doc.employee_advance_details;
		var total = 0;
		for(var i in table) {
			total = total + table[i].current_advance;
		}
		frm.set_value("total_advance_amount",total);
	}
})
frappe.ui.form.on("Employee Advance Details",{
	current_advance:function(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.current_advance > row.eligible_amount){
			frappe.msgprint({message: __("{0}  is greater than {1}",[row.current_advance,row.eligible_amount])});
			frappe.model.set_value(cdt,cdn,"current_advance",0)
		}
	}
})