// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Checkin Without Log Type', {
	refresh: function(frm) {
		cur_frm.add_custom_button('Create Employee Checkin', ()=>{
			var d = new frappe.ui.Dialog({
				title: "Create Employee Checkin",
				fields:[
					{fieldname:'from_date', label:'From Date', fieldtype:'Date', reqd:1, default:'Today'},
					{fieldtype:'Column Break'},
					{fieldname: 'to_date', label: 'To Date', fieldtype: 'Date', reqd:1, default:'Today'}
				],
				primary_action(r){
					if(r.from_date && r.to_date){
						frappe.call({
							method:'united_knitting_mills.ukm.utils.python.employee__checkin.create_employee_checkin',
							args:{
								from_date: r.from_date,
								to_date: r.to_date
							},
							freeze: true,
							freeze_message: 'Please wait Creating Employee Checkin.....'
						})
						d.hide();
					}
				}
			})
			d.show()
		})
	}
});
