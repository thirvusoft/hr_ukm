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

    if event == 'after_insert' or (event == 'validate' and not doc.is_new()):
        doc.total_shift_hr = 0
        doc.total_shift_count = 0
        if (doc.thirvu_shift_details):
            for data in doc.thirvu_shift_details:
                print(data.end_time,'11',data.start_time)
                # shift_hours =  get_datetime(data.end_time) - get_datetime(data.start_time)

                shift_hr = frappe.db.sql("""select timediff('{0}','{1}') as result""".format(data.end_time, data.start_time),as_list = 1)[0][0]
                # shift_hour = frappe.db.sql(''' select sec_to_time('{0}')'''.format(shift_hr),as_list = 1)[0][0]
                data.shift_hours =  shift_hr / datetime.timedelta(hours=1)
                # print(data.shift_hours)
                # doc.total_shift_hr += data.shift_hours
                # doc.total_shift_count += data.shift_count
        ee


    