import frappe, json
import datetime
from frappe.utils import cint, get_datetime, getdate, to_timedelta

def validate_shift_details(doc, event):
    shift_count(doc, event)
    shift_hours(doc, event)

def shift_count(doc,event):
    pass
    # doc.total_shift_count = 0
    # doc.total_shift_amount = 0
    # for data in doc.thirvu_shift_details:
    #     doc.total_shift_count += data.shift_count
    #     doc.total_shift_amount += data.shift_salary
    
def shift_hours(doc,event):
    doc.total_shift_hours = 0
    if event == 'after_insert' or (event == 'validate' and not doc.is_new()):
        if (doc.thirvu_shift_details):
            for data in doc.thirvu_shift_details:
                shift_hours =  get_datetime(data.end_time) -  get_datetime(data.start_time)
                data.shift_hours =  shift_hours / datetime.timedelta(hours=1)
                doc.total_shift_hours += data.shift_hours


def total_shift_amount(doc,event):
    employee_name = doc.employee
    doc.total_shift_amount = 0 
    shift_count = doc.thirvu_shift_details
    emp_base_amount=frappe.db.sql("""select ssa.base
				FROM `tabSalary Structure Assignment` as ssa
				WHERE ssa.employee = '{0}' ORDER BY ssa.creation DESC LIMIT 1
                """.format(employee_name),as_list=1)[0][0]
    for row in shift_count:
        count=row.shift_count
        shift_amount = count*emp_base_amount
        row.shift_salary = shift_amount
        doc.total_shift_amount += row.shift_salary

    