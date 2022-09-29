frappe.listview_settings['Employee Advance'] = {
	onload: function(listview) {
		listview.page.clear_menu()
    },
	get_indicator: function(doc) {
		var indicator = [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		indicator[1] = {"Draft": "brown", "Cancelled": "red", "Approved": "green","Unpaid":"orange","Paid":"orange"}[doc.status];
		return indicator;
	}
}