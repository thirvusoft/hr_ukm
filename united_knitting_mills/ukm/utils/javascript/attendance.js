var atte_date
var shift_count
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

    },
    refresh:function(frm){

        if (cur_frm.doc.workflow_state == "Present"){
        
            let r= cur_frm.add_custom_button("Make Shift Changes", async function() {
            atte_date=cur_frm.doc.attendance_date
            shift_count=cur_frm.doc.total_shift_count
            var name = cur_frm.doc.name
                await frappe.run_serially([
                    async () => {
                        await frappe.new_doc("Attendance Shift Changes", {
                            attendance:cur_frm.doc.name,
                            employee:cur_frm.doc.employee,
                            employee_name:cur_frm.doc.employee_name,
                            attendance_date:cur_frm.doc.attendance_date,
                            total_shift_count:cur_frm.doc.total_shift_count
                });
            },
                () =>{
                    cur_frm.set_value("attendance_date", atte_date)
                    cur_frm.set_value("total_shift_count", shift_count)
                },

                () => {
                    frappe.db.get_list("Employee Checkin",{filters:{"attendance":name}, fields:["time", "log_type"]}).then((list) => {
                        for (var i=0; i < list.length; i++){
                            let row = cur_frm.add_child("checkin_details");
                            row.time = list[i]["time"];
                            row.type = list[i]["log_type"];
                            cur_frm.refresh_field("checkin_details");
                        }
                        
                    })
                }
            ]);
            })
            r[0].style.backgroundColor="green"
            r[0].style.color="white"
        }
    }
    
})