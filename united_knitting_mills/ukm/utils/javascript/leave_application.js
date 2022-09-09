frappe.ui.form.on("Leave Application",{
	onload:function(frm){
        setTimeout(() => {
            frm.dashboard.hide();
        }, 1);
    }
})