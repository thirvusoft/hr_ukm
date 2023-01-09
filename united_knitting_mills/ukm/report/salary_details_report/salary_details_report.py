# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

from ctypes.wintypes import PFLOAT
import frappe
import pandas
from datetime import date, datetime, timedelta
from frappe import _
from erpnext.education.report.student_monthly_attendance_sheet.student_monthly_attendance_sheet import daterange

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    frappe.publish_realtime('refresh-report')
    return columns, data

def get_columns(filters):
    columns = [
         {
            "label": _("S.No"),
            "fieldtype": "Data",
            "fieldname": "sno",
            "width": 50
        },
        {
            "label": _("Employee ID"),
            "fieldtype": "Link",
            "fieldname": "code",
            "options":"Employee",
            "width": 110
        },
        {
            "label": _("Name of Employee"),
            "fieldtype": "Data",
            "fieldname": "worker_name",
            "width": 100
        },
        {
            "label": _("Designation"),
            "fieldtype": "Data",
            "fieldname": "designation",
            "width": 100
        },
        {
            "label": _("Account Number"),
            "fieldtype": "Data",
            "fieldname": "account_number",
            "width": 150
        },
        {
            "label": _("IFSC"),
            "fieldtype": "Data",
            "fieldname": "ifsc",
            "width": 100
        },
        {
            "label": _("Bank"),
            "fieldtype": "Data",
            "fieldname": "bank",
            "width": 100
        },
        {
            "label": _("Branch Name"),
            "fieldtype": "Data",
            "fieldname": "branch_name",
            "width": 120
        },
        {
            "label": _("Mode"),
            "fieldtype": "Data",
            "fieldname": "mode",
            "width": 80
        },
        
        {
            "label": _("Salary"),
            "fieldtype": "Currency",
            "fieldname": "salary",
            "width": 80
        },
        ]
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    staff_labour = filters['staff_labour']
    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))
    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
    for i in between_dates:
        
        columns.append({

            "label": i[len(i)-2:],
            "fieldtype": "Float",
            "fieldname": i,
            "print_width": 10
        })
    if staff_labour == "Labour":
            columns+=[
        {
            "label": _("Total Shift"),
            "fieldtype": "Float",
            "fieldname": "total_shift",
            "width": 100
        }]
    elif staff_labour == "Staff":
            columns+=[
        {
            "label": _("Total Working Days"),
            "fieldtype": "Float",
            "fieldname": "total_working_days",
            "width": 100
        },
         {
            "label": _("Total Paid Leave"),
            "fieldtype": "Float",
            "fieldname": "total_paid_leave",
            "width": 100
        },
         {
            "label": _("Total Present Days"),
            "fieldtype": "Float",
            "fieldname": "total_present_days",
            "width": 100
        }]

    columns+=[
        {
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "fieldname": "total_amount",
            "width": 100
        },
        {
            "label": _("Advance"),
            "fieldtype": "Currency",
            "fieldname": "advance",
            "width": 100
        },
        {
            "label": _("PF Deduction"),
            "fieldtype": "Currency",
            "fieldname": "pf_deduction",
            "width": 100
        },
        {
            "label": _("ESI Deduction"),
            "fieldtype": "Currency",
            "fieldname": "esi_deduction",
            "width": 100
        },
        {
            "label": _("Food Expense"),
            "fieldtype": "Currency",
            "fieldname": "tiffen",
            "width": 100
        },
        {
            "label": _("Medical Expense"),
            "fieldtype": "Currency",
            "fieldname": "medical_expense",
            "width": 100
        },
        {
            "label": _("Maintenance Expense"),
            "fieldtype": "Currency",
            "fieldname": "maintenance_expense",
            "width": 100
        },
        {
            "label": _("Rent Expense"),
            "fieldtype": "Currency",
            "fieldname": "rent_expense",
            "width": 100
        },
        {
            "label": _("Late Deduction"),
            "fieldtype": "Currency",
            "fieldname": "late_deduction",
            "width": 100
        },
        {
            "label": _("Total Deduction"),
            "fieldtype": "Currency",
            "fieldname": "total_deduction",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 80
        },
        {
            "label": _("Net Salary"),
            "fieldtype": "Currency",
            "fieldname": "net_salary",
            "width": 100
        },
        {
            "label": _("Signature"),
            "fieldtype": "Data",
            "fieldname": "signature",
            "width": 200
        },
        {
            "label": _("From Date"),
            "fieldtype": "Data",
            "fieldname": "from_date",
            "width": 200,
            "hidden":1
        },
        {
            "label": _("To Date"),
            "fieldtype": "Data",
            "fieldname": "to_date",
            "width": 200,
            "hidden":1
        }
    ]
    return columns
  

def get_data(filters):
    data=[]

    filter = {'start_date':["=", filters['from_date']],"end_date":["=", filters['to_date']],'docstatus':0}
    
    keys = list(filters.keys())

    from_date = filters["from_date"]
    to_date = filters["to_date"]
    staff_labour = filters['staff_labour']

    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))

    between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
   
    if ("designation" in keys):
        filter["designation"] = filters["designation"]

    if ("department" in keys):
        filter["department"] = filters["department"]

    if ("unit" in keys):
        filter["unit"] = filters["unit"]

    if ("status" in keys):

        if filters["status"] == "Yes":
            filter["is_hold"] = 1

        else:
            filter["is_hold"] = 0

    if staff_labour == "Staff":
        filter["is_staff_calulation"] = 1
        
    elif staff_labour == "Labour":
        filter["is_staff_calulation"] = 0

    ss=frappe.db.get_all("Salary Slip", filters=filter, fields=["name","employee","employee_name", "total_shift_worked","net_pay", "total_deduction","designation", "gross_pay","payment_days","leave_with_pay", "is_hold"],group_by="employee", order_by="designation")
    no=1
    non_hold=0
    for j in ss:
        f=frappe._dict()
        emp_doc = frappe.get_doc("Employee",j.employee)
        
        get_ssa=frappe.db.get_value("Salary Structure Assignment", {'employee':j.employee, 'docstatus':1}, 'base')

        if j["is_hold"]:
            hold = "Hold"
            non_hold=non_hold+j["net_pay"]
        else:
            hold = ""
            
        f.update(
            {   "sno":str(no),
                "code" : j['employee'],
                "worker_name":j.employee_name,
                "designation" : j.designation,
                "account_number" : emp_doc.bank_ac_no,
                "ifsc" : emp_doc.ifsc_code,
                "bank" : emp_doc.bank_name,
                "branch_name" : emp_doc.ts_bank_branch_name,
                "mode" : emp_doc.salary_mode,
                "status": hold,
                "salary":get_ssa
            }
        )

        for k in between_dates:
            get_attendance=frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'total_shift_count')
            f.update({k:get_attendance})
        salary_slip_detail=frappe.get_doc("Salary Slip",j.name)

        food_expence_count = 0
        pf_count = 0
        esi_count = 0
        advance_count = 0
        medical_expense_count = 0
        maintenance_expense_count = 0
        rent_expense_count = 0
        late_deduction_count = 0

        advance = 0
        food_expence = 0
        esi = 0
        pf = 0
        medical_expense = 0
        maintenance_expense = 0
        rent_expense = 0
        late_deduction = 0


        for x in range(0,len(salary_slip_detail.deductions),1):
            if food_expence_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Food Expense":
                    food_expence = salary_slip_detail.deductions[x].__dict__["amount"]
                    food_expence_count = 1
            
            if medical_expense_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Medical Expense":
                    medical_expense = salary_slip_detail.deductions[x].__dict__["amount"]
                    medical_expense_count = 1
            
            if maintenance_expense_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Maintenance Expense":
                    maintenance_expense = salary_slip_detail.deductions[x].__dict__["amount"]
                    maintenance_expense_count = 1

            if rent_expense_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Rent Expense":
                    rent_expense = salary_slip_detail.deductions[x].__dict__["amount"]
                    rent_expense_count = 1

            if late_deduction_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Late Deduction":
                    late_deduction = salary_slip_detail.deductions[x].__dict__["amount"]
                    late_deduction_count = 1

            if esi_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "ESI":
                    esi = salary_slip_detail.deductions[x].__dict__["amount"]
                    esi_count = 1

            if pf_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "PF":
                    pf = salary_slip_detail.deductions[x].__dict__["amount"]
                    pf_count = 1
 
            if advance_count == 0:
                if salary_slip_detail.deductions[x].__dict__["salary_component"] == "Employee Advance":
                    advance = salary_slip_detail.deductions[x].__dict__["amount"]
                    advance_count = 1

        if staff_labour == "Labour":
            f.update({"total_shift":j.total_shift_worked,"total_amount":j.gross_pay,"advance":advance,"tiffen":food_expence,"pf_deduction":pf,"esi_deduction":esi,"medical_expense":medical_expense, "maintenance_expense":maintenance_expense,"rent_expense":rent_expense,"late_deduction":late_deduction,"total_deduction":j.total_deduction,"net_salary":j.net_pay,"signature":'',"from_date":filters["from_date"],'to_date':filters["to_date"]})
        elif staff_labour == "Staff":
            f.update({"total_working_days":j.total_shift_worked,"total_paid_leave":j.leave_with_pay,"total_present_days":float(j.total_shift_worked) + j.leave_with_pay,"total_amount":j.gross_pay,"advance":advance,"tiffen":food_expence,"medical_expense":medical_expense, "maintenance_expense":maintenance_expense,"rent_expense":rent_expense,"late_deduction":late_deduction,"pf_deduction":pf,"esi_deduction":esi,"total_deduction":j.total_deduction,"net_salary":j.net_pay,"signature":'',"from_date":filters["from_date"],'to_date':filters["to_date"]})

        data.append(f)
        no+=1

    # data = [list(i.values()) for i in data]

    # designation_check = ''

    # for i in range (0, len(data), 1):
    #     if data[i][0] != designation_check:
    #         designation_check = data[i][0] 
    #         data[i][0] = f'<b>{data[i][0]}</b>'
           
    #     else:
    #         data[i][0] = ''
    if data :
        data.append({"status":"Total Hold Amount","net_salary":non_hold})
    return data

