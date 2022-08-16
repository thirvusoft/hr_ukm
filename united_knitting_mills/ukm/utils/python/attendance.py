import frappe, json
import datetime
from frappe.utils import cint, get_datetime, getdate, to_timedelta
 
def validate_shift_details(doc, event):
   shift_hours(doc, event)
 
  
def shift_hours(doc,event):
   if event == 'after_insert' or (event == 'validate' and not doc.is_new()):
       doc.total_shift_hr = 0
       doc.total_shift_count = 0
       if (doc.thirvu_shift_details):
           for data in doc.thirvu_shift_details:
               shift_hr = frappe.db.sql("""select timediff('{0}','{1}') as result""".format(data.end_time, data.start_time),as_list = 1)[0][0]
               shift_hours =  shift_hr / datetime.timedelta(hours=1)
               if shift_hours > 0:
                  data.shift_hours = shift_hours
               else:
                  hour_change = (to_timedelta('00:00:00') - to_timedelta(str(data.start_time))) + (to_timedelta('00:00:00') + to_timedelta(str(data.end_time)))
                  hour_change=str(hour_change)
                  hour_change=hour_change.split(", ")
                  data.shift_hours = to_timedelta(hour_change[1])/ datetime.timedelta(hours=1)
               doc.total_shift_hr += data.shift_hours
               doc.total_shift_count += data.shift_count
 
 
def total_shift_amount(doc,event):
   employee_name = doc.employee
#    doc.total_shift_amount = 0
#    shift_count = doc.thirvu_shift_details
#    emp_base_amount=frappe.db.sql("""select ssa.base
#                FROM `tabSalary Structure Assignment` as ssa
#                WHERE ssa.employee = '{0}' ORDER BY ssa.creation DESC LIMIT 1
#                """.format(employee_name),as_list=1)
#    if emp_base_amount:
#        emp_base_amount = emp_base_amount[0][0]
#        for row in shift_count:
#            count=row.shift_count
#            shift_amount = count*emp_base_amount
#            if frappe.db.get_value('Thirvu Shift Status',row.shift_status,'double_salary'):
#                row.shift_salary = shift_amount*2
#            else:
#                row.shift_salary = shift_amount
#            doc.total_shift_amount += row.shift_salary
