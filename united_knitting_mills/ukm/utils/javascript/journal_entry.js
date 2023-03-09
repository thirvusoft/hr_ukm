frappe.ui.form.on('Journal Entry Account',{
    account:function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if(row.account){
            if(row.account == 'Petty Cash 2 - UKM'){
                if(frappe.session.user == "annalakshmi@gmail.com"){
                    frappe.model.set_value(cdt,cdn,"location",'UNIT 2');
                }
                else{
                    frappe.db.get_value('Employee', {'user_id':frappe.session.user},['location'], function(data) {
                        frappe.model.set_value(cdt,cdn,'location',data.location);
                    })
                }
            }
            else if(row.account == 'Petty Cash 1 - UKM'){
                if(frappe.session.user == "annalakshmi@gmail.com"){
                    frappe.model.set_value(cdt,cdn,"location",'UNIT 1');
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
    },
    party:function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if (row.party_type == "Employee"){
            frappe.db.get_value(row.party_type,{"name":row.party},"employee_name").then((r)=>{
                frappe.model.set_value(cdt, cdn, "ts_party_name", r.message["employee_name"]);
            })
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
    }
})
