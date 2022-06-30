frappe.ui.form.on('Employee',{
    refresh:function(frm){
        if(!frm.is_dirty()){
        frm.add_custom_button(('Salary Structure Assignment'), function() {
            var doc = frappe.model.get_new_doc('Salary Structure Assignment');
            frappe.set_route('Form', 'Salary Structure Assignment', doc.name);
        }).addClass("btn-danger").css({'color':'white','background-color': 'grey','font-weight': 'bold'});
    }}
})