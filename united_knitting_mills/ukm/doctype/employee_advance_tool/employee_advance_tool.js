	
frappe.ui.form.on("Employee Advance Tool",{
	designation:function(frm,cdt,cdn){
		var advance=locals[cdt][cdn]
		var advance1=advance.designation
		frappe.db.get_value('Employee', {'user_id':frappe.session.user}, ['location','name'], function(data) {
			var location=data.location
			if(location){
				cur_frm.set_value('id',data.name)
				frappe.call({
					method:"united_knitting_mills.ukm.doctype.employee_advance_tool.employee_advance_tool.employee_finder",
					args:{advance1,location},
					callback(r){
						frm.clear_table("employee_advance_details");
						for(let i=0;i<r.message.length;i++){
							var child = cur_frm.add_child("employee_advance_details");
							frappe.model.set_value(child.doctype, child.name, "employee", r.message[i]["name"])
							frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i]["employee_name"])
							frappe.model.set_value(child.doctype, child.name, "designation", advance1)
							if (frm.doc.designation == "Labour Worker"){
								frappe.model.set_value(child.doctype, child.name, "payment_method",'Deduct from Salary')
							}
						}
						cur_frm.refresh_field("employee_advance_details")
					}
				})
			}
			else{
				frappe.msgprint('Location not assigned for this user')
			}
			
		});		

	},
	
	on_submit:function(frm,cdt,cdn){
		var advance=locals[cdt][cdn]
		for(let i=0;i<advance.employee_advance_details.length;i++){
			frappe.call({
				method:"united_knitting_mills.ukm.doctype.employee_advance_tool.employee_advance_tool.create_employee_advance",
				args:{amount:advance.employee_advance_details[i].current_advance,
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
