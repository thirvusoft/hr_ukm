// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Thirvu Shift', {
	refresh: function(frm) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__('Mark Employee Attendance'), function () {
				frappe.call({
					method: "united_knitting_mills.ukm.doctype.thirvu_shift.thirvu_shift.create_employee_attendance",
					args: {
						departments:frm.doc.department,
						doc:frm.doc.name,
						late_entry:frm.doc.entry_period,
						early_exit:frm.doc.exit_period
					},
				});
			}, __('Actions'));
		}
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
