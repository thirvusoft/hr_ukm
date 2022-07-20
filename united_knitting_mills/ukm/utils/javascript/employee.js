frappe.ui.form.on('Employee',{
    refresh:function(frm){
        cur_frm.add_fetch('location', 'select_naming_series', 'naming_series');
        if(!frm.is_dirty()){
            frm.add_custom_button(('Salary Structure Assignment'), function() {

                var doc = frappe.model.get_new_doc('Salary Structure Assignment');
                doc.employee=frm.doc.name
                frappe.set_route('Form', 'Salary Structure Assignment', doc.name)
                
            }).addClass("btn-danger").css({'color':'white','background-color': 'grey','font-weight': 'bold'});
            frm.add_custom_button(('Assign HR Permission'), function() {
                frappe.call({
                    method:"united_knitting_mills.ukm.utils.python.employee.creating_hr_permission",
                    args:{doc:frm.doc.name},
                    callback(r){
                        if(r.message===0){
                            frappe.show_alert({ message: __('HR Permission Created'), indicator: 'green' });
                        }
                        else if(r.message===1){
                            frappe.show_alert({ message: __('Already HR Permission Created'), indicator: 'red' });
                        }
                    }
                })

            }).addClass("btn-danger").css({'color':'white','background-color': 'orange','font-weight': 'bold'});
        }
        if(frm.is_new()){
            frm.set_value("hr_permission",0)
        }
}

})
