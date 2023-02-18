// Copyright (c) 2023, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Shift Changes', {
	onload: function(frm) {
		if (frm.doc.docstatus!=1 && frm.doc.attendance != '' && !frm.doc.__islocal){
			cur_frm.set_value('checkin_details',[])
			frappe.db.get_list("Employee Checkin",{filters:{"attendance":frm.doc.attendance}, fields:["time", "log_type"]}).then((list) => {
				for (var i=0; i < list.length; i++){
					let row = cur_frm.add_child("checkin_details");
					row.time = list[i]["time"];
					row.type = list[i]["log_type"];
					cur_frm.refresh_field("checkin_details");
					cur_frm.save()
				}
			})
		}
	}
});
