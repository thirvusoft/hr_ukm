frappe.ui.form.on('Employee',{
    refresh:async function(frm){
        if(!frm.is_dirty()){
            frm.add_custom_button(('Salary Structure Assignment'), function() {

                var doc = frappe.model.get_new_doc('Salary Structure Assignment');
                doc.employee=frm.doc.name
                frappe.set_route('Form', 'Salary Structure Assignment', doc.name)
                
            }).addClass("btn-danger").css({'color':'white','background-color': 'grey','font-weight': 'bold'});
        }
        if(frm.is_new()){
            frm.set_value("hr_permission",0)
        }
        if (in_list(frappe.user_roles, "Owner")) {
            frm.set_df_property("approval_by_owner", "hidden",0);
        }
        else{
            frm.set_df_property("approval_by_owner", "hidden",1);

        }
        frm.set_query('department',function(){
            return{
                filters:{
                    "unit":frm.doc.location
                }
            }
        })
        frm.set_query('designation',function(){
            return{
                filters:{
                    "unit":frm.doc.location
                }
            }
        })
        await frappe.db.get_single_value("United Knitting Mills Settings", "employment_type_for_commision_calculation").then((value) => {
            frm.set_query('commision_agent',function() {
           
            return{
                filters:{
                    "employment_type":value
                }
            }
            })
        })
        frappe.db.get_single_value("United Knitting Mills Settings", "employment_type_for_commision_calculation").then((value) => {
            if (value == frm.doc.employment_type){
                frm.set_df_property('employee_commision', 'hidden', 0);
            }
            else{

                frm.set_df_property('employee_commision', 'hidden', 1);
            }

    })
    },
    onload(frm){
        if(!frm.is_new() && frm.doc.ts_interview_details){
            if(!frm.doc.ts_interview_details.length){
                frappe.call({
                    method: 'united_knitting_mills.ukm.utils.python.employee.create_interview_details',
                    args:{name:frm.doc.name},
                    async:false,
                    callback(r){
                        cur_frm.reload_doc(); 
                    }
                })
            }
        }
    },
    employment_type: function(frm){
        frappe.db.get_single_value("United Knitting Mills Settings", "employment_type_for_commision_calculation").then((value) => {
            if (value == frm.doc.employment_type){
                frm.set_df_property('employee_commision', 'hidden', 0);
            }
            else{

                frm.set_df_property('employee_commision', 'hidden', 1);
            }

    })
    }

})
