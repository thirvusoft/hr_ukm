// Copyright (c) 2022, UKM and contributors
// For license information, please see license.txt

frappe.ui.form.on('United Knitting Mills Settings', {
	ts_create: function(frm) {
		frappe.call({
			method:"united_knitting_mills.ukm.doctype.united_knitting_mills_settings.united_knitting_mills_settings.creating_hr_permission"
		})
	}
});
