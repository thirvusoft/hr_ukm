
frappe.ui.form.on('Payroll Entry', {
	onload: function (frm) {
            if (!frm.doc.salary_slip_based_on_timesheet) {
                frappe.call({
                    method: 'erpnext.payroll.doctype.payroll_entry.payroll_entry.get_start_end_dates',
                    args: {
                        payroll_frequency: frm.doc.payroll_frequency,
                        start_date: frm.doc.posting_date
                    },
                    callback: function (r) {
                        if (r.message) {
                            in_progress = true;
                            frm.set_value('start_date', r.message.start_date);
                            frm.set_value('end_date', r.message.end_date);
                        }
                    }
                });
            }
    },
    refresh:function(frm){
        frm.set_query('designation',function(){
            return{
                filters:{
                    "unit":frm.doc.location
                }
            }
        })
        frm.set_query('department',function(){
            return{
                filters:{
                    "unit":frm.doc.location
                }
            }
        })
    }
})