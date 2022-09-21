frappe.ui.form.on('Attendance',{
    req_total_shift_count:function(frm){
        if(!frm.doc.staff){
            frappe.call({
                method:"united_knitting_mills.ukm.utils.python.attendance.get_shift_amount",
                args:{
                    employee:frm.doc.employee
                },
                callback:function(r){
                    cur_frm.set_value('req_total_shift_amount',r.message*frm.doc.req_total_shift_count)
                }
            })
        }
    }
})