// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Timing Details', {
	refresh: function(frm) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__('Mark Employee Attendance'), function () {
				frappe.call({
					method: "united_knitting_mills.ukm.doctype.thirvu_shift.thirvu_shift.create_employee_attendance",
					args: {
						departments:frm.doc.department,
						doc:frm.doc.name,
						location:frm.doc.unit,
						late_entry:frm.doc.entry_period,
						early_exit:frm.doc.exit_period
					},
					freeze:true,
					freeze_message: __("Creating Attendance..."),
				});
			}, __('Actions'));
		}
		// Check and Uncheck for labour and staff fields
		cur_frm.fields_dict.staff.$input.on('click', ()=>{
			uncheck(frm, 'labour')
		})
		cur_frm.fields_dict.labour.$input.on('click', ()=>{
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