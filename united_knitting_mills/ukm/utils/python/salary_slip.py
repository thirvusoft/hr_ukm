
import frappe
import erpnext
from frappe.utils import money_in_words

import json
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe import _
from frappe.utils.data import get_link_to_form
from united_knitting_mills.ukm.utils.python.employee import get_employee_shift

def set_salary_for_labour(doc,event):
    
    shift = get_employee_shift(doc.employee)
    shift_doc = frappe.get_doc('Employee Timing Details', shift)

    emp_base_amount=frappe.db.sql("""select ssa.base
                    FROM `tabSalary Structure Assignment` as ssa
                    WHERE ssa.employee = '{0}' and ssa.from_date >='{1}' and ssa.docstatus = 1
                    ORDER BY ssa.from_date DESC LIMIT 1 """.format(doc.employee,doc.start_date),as_list=1)
    
    if emp_base_amount:
        doc.ts_shift_amount = emp_base_amount[0][0]

    if(shift_doc.labour or shift_doc.house_keeping):
        salary_slip_for_labours(doc, event)
        food_expens_amount(doc)

    elif(shift_doc.staff):
        staff_salary_calculation(doc,event)
        food_expens_amount(doc)

@frappe.whitelist()
def salary_slip_for_labours(doc,event):

    """Salary Slip For Labours"""
    emp_shift_component=frappe.db.get_value("Salary Structure", doc.salary_structure, "salary_component_")
    
    emp_shift_amount = frappe.db.sql("""
            select sum(total_shift_amount),sum(total_shift_count),sum(total_shift_hr)
            from `tabAttendance`
            where employee=%s and attendance_date>=%s and attendance_date<=%s and workflow_state='Present'
        """, (doc.employee, doc.start_date, doc.end_date), as_list = 1)

    if emp_shift_amount[0][1]:
        doc.total_shift_worked = emp_shift_amount[0][1]

    if emp_shift_amount[0][0]:
        
        doc.total_shift_minutes = emp_shift_amount[0][2]
        
        for row in doc.earnings:
            if row.salary_component == emp_shift_component:
                doc.earnings[row.idx -1].update( {"salary_component": emp_shift_component, "amount":emp_shift_amount[0][0] })
        
        if len(doc.earnings) == 0:
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

def staff_salary_calculation(doc,event):

    if not doc.is_staff_calulation:

        if doc.department:
            department = doc.department
            department_doc = frappe.get_doc("Department",department)

            if department_doc.is_staff:
                salary_structure_assignment = frappe.get_value("Salary Structure Assignment",{"employee":doc.employee,"docstatus":1},["base"])

                atte = sum(frappe.db.get_all("Attendance", filters={'employee':doc.employee,'attendance_date':['between',(doc.start_date, doc.end_date)],'workflow_state':"Present", "sunday_attendance": 0}, pluck='total_shift_count'))
                atte = atte + sum(frappe.db.get_all("Attendance", filters={'employee':doc.employee,'attendance_date':['between',(doc.start_date, doc.end_date)],'workflow_state':"Present", "sunday_attendance": 1, "sunday_approval":1}, pluck='total_shift_count'))
                
                doc.total_shift_worked = atte
                
                doc.per_day_salary_for_staff = salary_structure_assignment/doc.total_working_days
                salary_for_persent_days = doc.per_day_salary_for_staff * doc.total_shift_worked
                
                doc.append("earnings",{"salary_component":"Basic",
                    "amount":salary_for_persent_days})

                gross_salary = salary_for_persent_days

                #  Pay Leave Adding in Salary Slip
                pay_leave_details = add_pay_leave(doc.start_date, doc.end_date, doc.employee, doc.per_day_salary_for_staff)
                
                if pay_leave_details[1] != 0:
                    
                    doc.leave_with_pay = pay_leave_details[1]
                    doc.append("earnings",{"salary_component":"Pay Leave",
                        "amount":pay_leave_details[0]})

                    gross_salary += pay_leave_details[0]

                doc.gross_pay = gross_salary
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
                
        
@frappe.whitelist()
def add_pay_leave(start_date, end_date, employee, per_day_salary_for_staff = None):

    pay_leave = frappe.get_all("Leave Application",{
                    "employee": employee,
                    "is_pay_leave_application": 1,
                    "status": "Approved",
                    "docstatus": 1,
                    "from_date": ["between", (start_date, end_date)]
                    },
                "name")

    if not per_day_salary_for_staff:
        per_day_salary_for_staff = 0

    return len(pay_leave) * per_day_salary_for_staff, len(pay_leave)

def food_expens_amount(doc):

    if not doc.expense_updated:

        settings = frappe.get_single("United Knitting Mills Settings")

        employee_doc=frappe.db.get_all("Employee", filters={"name":doc.employee, "status":"Active"}, fields=["gender"])
        
        if doc.food_expense_days:

            if employee_doc and employee_doc[0]["gender"] == "Male":
                doc.food_expense_amount=settings.amount_for_male_employee

            elif employee_doc and employee_doc[0]["gender"] == "Female":
                doc.food_expense_amount=settings.amount_for_female_employee

            else:
                doc.food_expense_amount=0

        doc.update({'deductions':
            [
                {'salary_component':"Food Expense", 'amount':(doc.food_expense_days or 0)*(doc.food_expense_amount or 0)},
                {'salary_component':"Medical Expense", 'amount':doc.medical_expense},
                {'salary_component':"Maintenance Expense", 'amount':doc.maintenance_expense},
                {'salary_component':"Rent Expense", 'amount':doc.rent_expense },
                {'salary_component':"Late Deduction", 'amount': doc.late_deduction}
            ]
        })

        doc.expense_updated = 1
        SalarySlip.calculate_net_pay(doc)
