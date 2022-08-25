import frappe, json
import datetime
from datetime import datetime as dt
from frappe.utils import cint, get_datetime, getdate, to_timedelta
from erpnext.hr.doctype.attendance.attendance import Attendance
from united_knitting_mills.ukm.utils.python.employee import get_employee_shift

def validate_shift_details(doc, event):
   shift_hours(doc, event)
 
  
def shift_hours(doc,event):
   shift = get_employee_shift(doc.employee)
   labour = frappe.db.get_value("Employee Timing Details", shift, 'labour')
   if labour and (event == 'after_insert' or (event == 'validate' and not doc.is_new())):
       doc.total_shift_hr = 0
       doc.total_shift_count = 0
       doc.total_shift_amount = 0
       if(doc.thirvu_shift_details):
           for data in doc.thirvu_shift_details:
               shift_hr = frappe.db.sql("""select timediff('{0}','{1}') as result""".format(data.end_time, data.start_time),as_list = 1)[0][0]
               shift_hours =  shift_hr / datetime.timedelta(hours=1)
               if shift_hours > 0:
                  if(not data.get('shif_hours')):
                     data.shift_hours = shift_hours
                  doc.total_shift_hr += shift_hr / datetime.timedelta(minutes=1)
               else:
                  diff_time = (to_timedelta(str(data.end_time)) - to_timedelta(str(data.start_time)))
                  if(not data.get('shif_hours')):
                     data.shift_hours = diff_time/ datetime.timedelta(hours=1)
                  doc.total_shift_hr +=  diff_time / datetime.timedelta(minutes=1)
               doc.total_shift_count += data.shift_count
               doc.total_shift_amount += data.shift_salary
           if(doc.total_shift_hr):
               doc.total_shift_hr -= get_total_break_time(doc.employee)
def unlink_logs(doc,event):
   Attendance.unlink_attendance_from_checkins(doc)

def get_total_break_time(employee):
   shift = get_employee_shift(employee)
   thirvu_shift = frappe.get_doc('Employee Timing Details', shift)
   if(not thirvu_shift.is_break_times_are_included_with_shift_times): return 0
   break_time = thirvu_shift.break_time
   FMT = '%H:%M:%S'
   tot_brk_time =sum( (dt.strptime(str(row.end_time), FMT) - dt.strptime(str(row.start_time), FMT))/datetime.timedelta(minutes=1) for row in break_time if(row.start_time and row.end_time)) or 0
   return tot_brk_time