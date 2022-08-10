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

frappe.ui.form.on('Journal Entry',{
    setup:function(frm,cdt,cdn){
        frappe.call({
            method:"united_knitting_mills.ukm.utils.python.journal_entry.get_user_location",
			args: {"user": frappe.session.user},
			callback:function(r){
                if (r.message.length){
                    frm.set_query('account', 'accounts',function(doc) {
                        return {
                            filters: {'location':['in',r.message]
                            }
                        };
                    });
                }
			}

        })


        // // frappe.session.user
        // frm.set_query('account', 'accounts',function(doc) {
        //     return {
        //         filters: {
        //             location
        //         }
        //     };
        // });
    }
})