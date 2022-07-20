frappe.ui.form.on('Journal Entry Account',{
    account:function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if(row.account){
            if(row.account == 'Petty Cash 2 - UKM'){
                if(frappe.session.user == "annalakshmi@gmail.com"){
                    frappe.model.set_value(cdt,cdn,"location",'');
                }
                else{
                    frappe.db.get_value('Employee', {'user_id':frappe.session.user},['location'], function(data) {
                        frappe.model.set_value(cdt,cdn,'location',data.location);
                    })
                }
            }
            else{
                frappe.db.get_value('Employee', {'user_id':frappe.session.user},['location'], function(data) {
                    frappe.model.set_value(cdt,cdn,'location',data.location);
                })
            }
        } 
        else{
            frappe.model.set_value(cdt,cdn,"location",'');
        }
        }
})