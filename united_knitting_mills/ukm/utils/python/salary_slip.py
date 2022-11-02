
import frappe
import erpnext
from frappe.utils import money_in_words

import json
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe import _
from frappe.utils.data import get_link_to_form
from united_knitting_mills.ukm.utils.python.employee import get_employee_shift

def set_salary_for_labour_staff(doc,event):
    
    shift = get_employee_shift(doc.employee)
    shift_doc = frappe.get_doc('Employee Timing Details', shift)

    emp_base_amount=frappe.db.sql("""select ssa.base
                    FROM `tabSalary Structure Assignment` as ssa
                    WHERE ssa.employee = '{0}' and ssa.from_date >='{1}'
                    ORDER BY ssa.from_date DESC LIMIT 1 """.format(doc.employee,doc.start_date),as_list=1)
    if emp_base_amount:
        doc.ts_shift_amount = emp_base_amount[0][0]
    if(shift_doc.labour):
        salary_slip_for_labours(doc, event)
    # elif(shift_doc.staff or shift_doc.house_keeping):
    #     salary_slip_for_staffs(doc, event)

@frappe.whitelist()
def salary_slip_for_labours(doc,event):
    """Salary Slip For Labours"""
    emp_shift_component=frappe.db.get_value("Salary Structure", doc.salary_structure, "salary_component_")
    emp_shift_amount = frappe.db.sql("""
            select sum(total_shift_amount),sum(total_shift_count),sum(total_shift_hr)
            from `tabAttendance`
            where employee=%s and attendance_date>=%s and attendance_date<=%s and docstatus = 1
        """, (doc.employee, doc.start_date, doc.end_date), as_list = 1)
    if(emp_shift_amount[0][0]):
        doc.total_shift_worked = emp_shift_amount[0][1]
        doc.total_shift_minutes = emp_shift_amount[0][2]
        # doc.set('earnings', [])
        for row in doc.earnings:
            if(row.salary_component == emp_shift_component):
                doc.earnings[row.idx -1].update( {"salary_component": emp_shift_component, "amount":emp_shift_amount[0][0] })
        if(len(doc.earnings) == 0):
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

# def salary_slip_for_staffs(doc, event):
    # """Salary Slip For Staff"""
    # emp_shift_amount = frappe.db.sql("""
    #         select sum(total_shift_amount),sum(ts_ot_hrs),sum(total_shift_hr)
    #         from `tabAttendance`
    #         where employee=%s and attendance_date>=%s and attendance_date<=%s and docstatus = 1
    #     """, (doc.employee, doc.start_date, doc.end_date), as_list = 1)
    # if(emp_shift_amount[0][0]):
    #     doc.extra_minutes = emp_shift_amount[0][1]
    #     doc.total_shift_minutes = emp_shift_amount[0][2]
    #     emp_shift_component=frappe.db.get_value("Salary Structure", doc.salary_structure, "salary_component_")
    #     # doc.set('earnings', [])
    #     for row in doc.earnings:
    #         if(row.salary_component == emp_shift_component):
    #             doc.earnings[row.idx -1].update( {"salary_component": emp_shift_component, "amount":emp_shift_amount[0][0] })
    #     if(len(doc.earnings) == 0):
    #         doc.append("earnings", {"salary_component": emp_shift_component, "amount":emp_shift_amount[0][0] })
        # gross_pay=0
        # for data in doc.earnings:
        #     gross_pay+=data.amount
        
        # doc.gross_pay=gross_pay
        # doc.net_pay=doc.gross_pay-doc.total_deduction
        # doc.rounded_total=round(doc.net_pay)    

        #Calculation of year to date
        # SalarySlip.compute_year_to_date(doc)
        
        #Calculation of Month to date
        # SalarySlip.compute_month_to_date(doc)
        # SalarySlip.compute_component_wise_year_to_date(doc)
        # SalarySlip.set_net_total_in_words(doc)
    
    

def create_journal_entry(doc,action):
    earn_component_list=[]
    earn_amount=[]
    ded_component_list=[]
    ded_amount=[]
    location = frappe.db.get_value('Employee', doc.employee, 'location')
    if doc.earnings:
        for data in doc.earnings:
            account = frappe.get_doc('Salary Component',data.salary_component)
            url = get_link_to_form('Salary Component',data.salary_component)
            if(not len(account.accounts)):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
            for row in account.accounts:
                if(row.company == doc.company):
                    if(not row.account):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
                    earn_component_list.append(row.account)
            earn_amount.append(data.amount)

    if doc.deductions:
        for data in doc.deductions:
            account = frappe.get_doc('Salary Component',data.salary_component)
            url = get_link_to_form('Salary Component',data.salary_component)
            if(not len(account.accounts)):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
            for row in account.accounts:
                if(row.company == doc.company):
                    if(not row.account):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
                    ded_component_list.append(row.account)
            ded_amount.append(data.amount)

    new_jv_doc=frappe.new_doc('Journal Entry')
    new_jv_doc.voucher_type='Journal Entry'
    new_jv_doc.posting_date=doc.posting_date
    new_jv_doc.company = doc.company
    new_jv_doc.user_remark = _("Accrual Journal Entry for salaries from {0} to {1}").format(
                doc.start_date, doc.end_date
            )
    for data in range(0,len(earn_component_list),1):
        new_jv_doc.append('accounts',{'account':earn_component_list[data],'debit_in_account_currency':earn_amount[data], 'location':location})
    for data in range(0,len(ded_component_list),1):
        new_jv_doc.append('accounts',{'account':ded_component_list[data],'credit_in_account_currency':ded_amount[data], 'location':location})
    if(frappe.db.get_value("Company",doc.company, "default_payroll_payable_account")):
        new_jv_doc.append('accounts',{'account':frappe.db.get_value("Company",doc.company, "default_payroll_payable_account"),'credit_in_account_currency':doc.net_pay, 'location':location})
    else:
        frappe.msgprint(_("Set Default Payable Account in {0}").format(doc.company), alert=True)
    # new_jv_doc.insert()
    # new_jv_doc.submit()

def staff_salary_calculation(doc,event):

    if not doc.is_staff_calulation:
        print("helooo")
        if doc.department:
            department = doc.department
            department_doc = frappe.get_doc("Department",department)

            if department_doc.is_staff:
                salary_structure_assignment = frappe.get_value("Salary Structure Assignment",{"employee":doc.employee},["base"])
                
                per_day_salary = salary_structure_assignment/doc.total_working_days
                salary_for_persent_days = per_day_salary * doc.payment_days
                doc.append("earnings",{"salary_component":"Basic",
                    "amount":salary_for_persent_days})

                doc.gross_pay = salary_for_persent_days
                doc.net_pay = doc.gross_pay - doc.total_deduction
                doc.rounded_total = round(doc.net_pay)

                company_currency = erpnext.get_company_currency(doc.company)
                total = doc.net_pay if doc.is_rounding_total_disabled() else doc.rounded_total
                base_total = doc.base_net_pay if doc.is_rounding_total_disabled() else doc.base_rounded_total
                doc.total_in_words = money_in_words(total, doc.currency)
                doc.base_total_in_words = money_in_words(base_total, company_currency)

                # Calculation of year to date
                SalarySlip.compute_year_to_date(doc)
                
                #Calculation of Month to date
                SalarySlip.compute_month_to_date(doc)
                SalarySlip.compute_component_wise_year_to_date(doc)
                SalarySlip.set_net_total_in_words(doc)
                doc.is_staff_calulation = 1

    else:

        gross_pay = 0
        for data in doc.earnings:
            gross_pay += data.amount
        
        doc.gross_pay = gross_pay
        doc.net_pay = doc.gross_pay-doc.total_deduction
        doc.rounded_total = round(doc.net_pay)

        # Calculation of year to date
        SalarySlip.compute_year_to_date(doc)
        
        #Calculation of Month to date
        SalarySlip.compute_month_to_date(doc)
        SalarySlip.compute_component_wise_year_to_date(doc)
        SalarySlip.set_net_total_in_words(doc)
                
        