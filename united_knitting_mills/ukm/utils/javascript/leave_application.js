frappe.ui.form.on("Leave Application",{
	onload:function(frm){
        setTimeout(() => {
            frm.dashboard.hide();
        }, 1);
    },

    setup:function(frm){
        frappe.call({
            method:"united_knitting_mills.ukm.utils.python.leave_application.employee_staff_filter",
            
            callback: function(r){
                if ((r.message).length !=0){

                    var staff_employee = r.message

                    frm.set_query("employee",function(){
                        return {

                            filters: [
                                ['Employee', 'name', 'in', staff_employee],
                            ]
                        };
                    });
                }
            }
        })
    },

    after_save:function(frm){
        if(frm.doc.docstatus != 1){
            if(frm.doc.status == "Rejected" || frm.doc.status == "Approved"){
                cur_frm.savesubmit()
            }
        }
    }
})