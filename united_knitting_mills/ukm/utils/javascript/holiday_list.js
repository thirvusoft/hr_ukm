frappe.ui.form.on("Holiday List",{
	onload:function(frm){
        setTimeout(() => {
            frm.dashboard.hide();
        }, 1);
    }
})