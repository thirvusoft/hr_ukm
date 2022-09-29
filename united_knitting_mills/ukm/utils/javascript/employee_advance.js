frappe.ui.form.on("Employee Advance",{
    onload:function(frm){
        setTimeout(() => {
            frm.dashboard.hide();
        }, 2);
    },
    employee:function(frm,cdt,cdn){
        var main_data=locals[cdt][cdn]
        if(main_data.employee){
            var employee=main_data.employee
            frappe.call({
                method:"united_knitting_mills.ukm.utils.python.employee_advance.advance_validation",
                args:{employee:employee},
                callback(eligible_amount){
                    if(eligible_amount){
                        frm.set_value("eligible_amount",eligible_amount.message)
                    }
                }
            })
        }
        else{
            frm.set_value("eligible_amount",0)
        }
    }
})