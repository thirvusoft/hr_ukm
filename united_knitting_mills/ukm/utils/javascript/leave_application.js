frappe.ui.form.on("Leave Application",{
	onload:function(frm){
        setTimeout(() => {
            frm.dashboard.hide();
        }, 1);
    },
    employee:function(frm){
        frappe.call({
            method:"united_knitting_mills.ukm.utils.python.leave_application.leave_type_filter",
            args:{department:frm.doc.department},
            callback: function(r){
                if ((r.message).length !=0){

                    var leave_type_list = r.message
                    frm.set_query("leave_type",function(){
                        return {
                            filters: [
                                ['Leave Type', 'name', 'in', leave_type_list],
                            ]
                        };
                    });
                }
            }
        })
           

    },
})