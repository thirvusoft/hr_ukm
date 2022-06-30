frappe.ui.form.on('Salary Structure Assignment',{
    refresh:function(frm){
        if (!frm.is_dirty()) {
        frm.add_custom_button(('Next'), function() {
            var doc = frappe.model.get_new_doc('Payroll Entry');
            frappe.set_route('Form', 'Payroll Entry', doc.name);
        }).addClass("btn-danger");
    }}
})