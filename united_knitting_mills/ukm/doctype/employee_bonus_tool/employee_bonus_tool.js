// Copyright (c) 2022, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Bonus Tool", {
	from_date: function (frm) {
		frm.set_value("emp_department", "")
	},
	to_date: function (frm) {
		frm.set_value("emp_department", "")
	},
	location: function (frm) {
		frm.set_value("emp_department", "")
	},
	get_employee_details: function (frm) {
		var emp_department = frm.doc.emp_department
		if (emp_department) {
			var from_date = frm.doc.from_date
			var to_date = frm.doc.to_date
			var location = frm.doc.location
			var designation = frm.doc.designation
			frappe.call({
				method: "united_knitting_mills.ukm.doctype.employee_bonus_tool.employee_bonus_tool.employee_finder",
				freeze: true,
				freeze_message: 'Fetching employee details...',
				args: { emp_department, designation, location, from_date, to_date },
				callback(r) {
					frm.set_value('employee_bonus_details', r.message)
					cur_frm.refresh_field("employee_bonus_details")
				}
			})
		}
		else {
			frm.clear_table("employee_bonus_details");
			cur_frm.refresh_field("employee_bonus_details")
			frm.set_value("total_bonus_amount", 0)
		}

	},
});

frappe.ui.form.on("Employee Bonus Details", {
	bonus_percentage: function(frm, cdt, cdn){
		var row=locals[cdt][cdn]
		if (row.salary) {
		frappe.model.set_value(cdt, cdn, 'current_bonus', (row.bonus_percentage/ 100) * row.salary)
		frappe.model.set_value(cdt, cdn, 'total_bonus_amount', (((row.bonus_percentage/ 100) * row.salary)+(row.settlement_salary)+(row.leave_salary)+(row.pay_leave_salary)))
		}
	}
})

