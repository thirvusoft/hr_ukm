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
    },
    before_save:function(frm){
        if (cur_frm.doc.req_checkin_time){
            cur_frm.set_value('time1',1)
        }
        else{
            cur_frm.set_value('time1',0)

        }
        if (cur_frm.doc.req_checkout_time){
            cur_frm.set_value('time2',1)
        }
        else{
            cur_frm.set_value('time2',0)
        }

    }
})