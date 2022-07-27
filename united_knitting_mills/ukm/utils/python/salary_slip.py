
import frappe
import json
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe import _

@frappe.whitelist()
def salary_slip_based_on_shift(doc,event):

    emp_struct=frappe.db.get_value("Salary Structure", doc.salary_structure, "salary_slip_based_on_shift")
    emp_shift_component=frappe.db.get_value("Salary Structure", doc.salary_structure, "salary_component_")

    emp_shift_amount = frappe.db.sql("""
			select sum(total_shift_amount),sum(total_shift_count)
			from `tabAttendance`
			where employee=%s and attendance_date>=%s and attendance_date<=%s
		""", (doc.employee, doc.start_date, doc.end_date), as_list = 1)
        
    if emp_struct==1:
        doc.total_shift_worked = emp_shift_amount[0][1]
        doc.set('earnings', [])
        doc.append("earnings", {"salary_component": emp_shift_component, "amount":emp_shift_amount[0][0] })
        gross_pay=0
        for data in doc.earnings:
            gross_pay+=data.amount
        
        doc.gross_pay=gross_pay
        doc.net_pay=doc.gross_pay-doc.total_deduction
        doc.rounded_total=round(doc.net_pay)    

        #Calculation of year to date
        SalarySlip.compute_year_to_date(doc)
        
        #Calculation of Month to date
        SalarySlip.compute_month_to_date(doc)
        SalarySlip.compute_component_wise_year_to_date(doc)
        SalarySlip.set_net_total_in_words(doc)

def create_journal_entry(doc,action):
    component_list=[]
    amount=[]
    if doc.earnings:
        for data in doc.earnings:
            account = frappe.get_doc('Salary Component',data.salary_component)
            for account in account.accounts:
                component_list.append(account.account)
            amount.append(data.amount)

    if doc.deductions:
        for data in doc.deductions:
            account = frappe.get_doc('Salary Component',data.salary_component)
            for account in account.accounts:
                component_list.append(account.account)
            amount.append(data.amount)

    new_jv_doc=frappe.new_doc('Journal Entry')
    new_jv_doc.voucher_type='Journal Entry'
    new_jv_doc.posting_date=doc.posting_date
    new_jv_doc.company = doc.company
    new_jv_doc.user_remark = _("Accrual Journal Entry for salaries from {0} to {1}").format(
				doc.start_date, doc.end_date
			)
    for data in range(0,len(component_list),1):
        new_jv_doc.append('accounts',{'account':component_list[data],'debit_in_account_currency':amount[data]})
    if(frappe.db.get_value("Company",doc.company, "default_payroll_payable_account")):
        new_jv_doc.append('accounts',{'account':frappe.db.get_value("Company",doc.company, "default_payroll_payable_account"),'credit_in_account_currency':doc.net_pay})
    else:
        frappe.msgprint(_("Set Default Payable Account in {0}").format(doc.company), alert=True)
    new_jv_doc.insert()
    new_jv_doc.submit()
