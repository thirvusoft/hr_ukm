// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Timing Details', {
	refresh: function(frm) {
		// if(!frm.doc.__islocal){
		// 	frm.add_custom_button(__('Mark Employee Attendance'), function () {
		// 		if(frm.doc.labour){
		// 		frm.call({
		// 			method: "create_labour_attendance",
		// 			args: {
		// 				departments:frm.doc.department,
		// 				doc:frm.doc.name,
		// 				location:frm.doc.unit,
		// 				late_entry:frm.doc.entry_period,
		// 				early_exit:frm.doc.exit_period
		// 				},
		// 			freeze:true,
		// 			freeze_message: __("Creating Attendance..."),
		// 			});
		// 			}
		// 			else if(frm.doc.staff || frm.doc.house_keeping){
		// 				frm.call({
		// 					method: 'create_staff_attendance',
		// 					args:{
		// 						docname: frm.doc.name
		// 					},
		// 					freeze:true,
		// 					freeze_message: __("Creating Attendance..."),
		// 					callback(r){
		// 					}
		// 				})
		// 			}
		// 	}, __('Actions'));
		// }
		// Check and Uncheck for labour and staff fields
		cur_frm.fields_dict.staff.$input.on('click', ()=>{
			uncheck(frm, 'labour')
			uncheck(frm, 'house_keeping')
		})
		cur_frm.fields_dict.labour.$input.on('click', ()=>{
			uncheck(frm, 'staff')
			uncheck(frm, 'house_keeping')
		})
		cur_frm.fields_dict.house_keeping.$input.on('click', ()=>{
			uncheck(frm, 'labour')
			uncheck(frm, 'staff')
		})
	},
	setup:function(frm){
		frm.set_query('shift_status', 'thirvu_shift_details', function() {
			return {
				'filters': {
					'unit': ['=', frm.doc.unit]
				}
			};
		});
	}
});

function uncheck(frm, field){
	frm.set_value(field, 0)
	frm.refresh_field(field)
}