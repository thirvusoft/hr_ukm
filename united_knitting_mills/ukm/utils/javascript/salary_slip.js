frappe.ui.form.on("Salary Slip",{
    
    add_pay_leave:function(frm){
        var data = frm.doc.earnings
        var match = 0

        frappe.call({
            method:"united_knitting_mills.ukm.utils.python.salary_slip.add_pay_leave",
            args:{start_date:frm.doc.start_date,to_date:frm.doc.end_date,employee:frm.doc.employee,per_day_salary_for_staff:frm.doc.per_day_salary_for_staff},
            callback(r){
                
                if (r.message){

                    for(var i = 0; i < data.length; i++){

                        if(data[i]["salary_component"] == "Pay Leave"){
                            match = 1
                            frm.set_value("leave_with_pay",r.message[1])
                            frappe.model.set_value(data[i].doctype,data[i].name,"amount",r.message[0])
                        }

                        else{
                            if(i == (data.length - 1) && match == 0){
                                cur_frm.add_child("earnings")
                                var index = data[i+1]
                                frappe.model.set_value(data[i+1].doctype,data[i+1].name,"salary_component","Pay Leave")
                                
                                setTimeout(() => {
                                frappe.model.set_value(index.doctype,index.name,"amount",r.message[0])
                                },650)
                                frm.set_value("leave_with_pay",r.message[1])
                            }
                        }
                    }
                }

                else{
                    frappe.msgprint("There Is No Pay Leave For This Employee And The Given Date Range.")
                }
            }
        })
    }
})