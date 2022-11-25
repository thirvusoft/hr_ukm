import frappe

@frappe.whitelist()
def salary_updation(doc, event):

    att_docs = frappe.get_all("Attendance", {"employee" : doc.employee,"docstatus" : 1})

    for att_doc in att_docs:
        att = frappe.get_doc("Attendance", att_doc)
        
        if not att.staff:

            if att.total_shift_amount == 0:
                att.total_shift_amount = att.total_shift_count * doc.base
                att.save()

def salary_updation_old():

        ssa_docs = frappe.get_all("Salary Structure Assignment",{"docstatus" : 1})

        for ssa_doc in ssa_docs:

            ssa_base = frappe.get_doc("Salary Structure Assignment", ssa_doc)
            att_docs = frappe.get_all("Attendance", {"employee" : ssa_base.employee,"docstatus" : 1})

            for att_doc in att_docs:
                att = frappe.get_doc("Attendance", att_doc)

                if not att.staff:
                    
                        att.total_shift_amount = att.total_shift_count * ssa_base.base
                        att.save()

# def salary_updation_old():

#         ssa_docs = frappe.get_all("Salary Structure Assignment",{"docstatus" : 1})

#         for ssa_doc in ssa_docs:

#             ssa_base = frappe.get_doc("Salary Structure Assignment", ssa_doc)
#             att_docs = frappe.get_all("Attendance", 
#             {
#                 "employee" : ssa_base.employee,
#                 "docstatus" : 1,
#                 "attendance_date":["between",("10-11-2022","23-11-2022")],
#                 "workflow_state":"Present",
#                 "total_shift_amount":0
#             })

#             for att_doc in att_docs:
#                 att = frappe.get_doc("Attendance", att_doc)

#                 if not att.staff:
                    
#                         att.total_shift_amount = att.total_shift_count * ssa_base.base

#                         if att.total_shift_amount != 0:
#                             att.save()



