frappe.ui.form.on('Location',{
    onload:function(frm){
        if(frm.doc.abbr)
            location(frm)
    },
    abbr:function(frm){
        if(frm.doc.abbr)
            location(frm)
    },
})
