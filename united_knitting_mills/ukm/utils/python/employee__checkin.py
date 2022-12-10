import frappe
from datetime import date, datetime, timedelta
import pandas
from frappe.utils import today
from united_knitting_mills.ukm.doctype.employee_timing_details.employee_timing_details import scheduler_for_employee_shift
def get_ukm_settings():
    buffer_time = frappe.db.get_single_value('United Knitting Mills Settings', 'buffer_time')
    reset_time = frappe.db.get_single_value('United Knitting Mills Settings', 'checkin_type_resetting_time')
    return buffer_time, reset_time

def get_between_dates(date_wise_checkin, from_date, to_date):
    from_d = tuple(map(int, from_date.split('-')))
    to_d = tuple(map(int, to_date.split('-')))
    between_dates = list(pandas.date_range(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2]),freq='d'))
    for data in between_dates:
        date_wise_checkin[str(data)]=[]
    return date_wise_checkin
    
def get_datewise_checkins_of_employee(date_wise_checkin, employee, reset_time):
    # last_checkin = frappe.get_last_doc('Employee Checkin', {'employee': employee})
    date_format_str = '%Y-%m-%d %H:%M:%S'
    reset_time = datetime.strptime(str(reset_time),'%H:%M:%S')
    for dates in date_wise_checkin:
        curr_date = datetime.strptime(str(dates), date_format_str)
        start_date = datetime.combine(curr_date.date(), reset_time.time())
        end_date = datetime.combine(curr_date.date() + timedelta(days = 1), reset_time.time())
        checkins = frappe.db.sql(f'''select name, time
                        from `tabEmployee Checkin Without Log Type`
                        where time >= '{start_date}' and time <= '{end_date}' and employee = '{employee}'
                        order by time''', as_list=1)
        checkins = [[i[0],i[1]] for i in checkins]
        date_wise_checkin[dates] += checkins
    return date_wise_checkin

# def validate_with_buffer_time(date_wise_checkin, buffer_time):
#     date_format_str = '%Y-%m-%d %H:%M:%S'
#     final_dict = frappe._dict()
#     for dates in date_wise_checkin:
#         final_names = []
#         times = [str(i[1]) for i in date_wise_checkin[dates]]
#         names = [str(i[0]) for i in date_wise_checkin[dates]]
#         times = list(set(times))
#         print(times)
#         for i in  range(len(times)):
#             curr_time = datetime.strptime(times[i], date_format_str)
#             final_time = curr_time + timedelta(minutes=buffer_time)
#             final_time_str = final_time.strftime(date_format_str)
#         final_dict[dates]=[]

def create_employee_checkins(date_wise_checkin, employee, buffer_time):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    log_type = ''
    for dates in date_wise_checkin:
        log = True
        create_checkin = True
        for i in range(len(date_wise_checkin[dates])):
            if(log == True):log_type="IN"
            else:log_type="OUT"
            if(i>0):
                curr_time = datetime.strptime(str(date_wise_checkin[dates][i-1][1]), date_format_str)
                final_time = curr_time + timedelta(minutes=buffer_time)
                final_time_str = final_time.strftime(date_format_str)
                if(str(date_wise_checkin[dates][i][1]) >= final_time_str):
                    create_checkin = True
                else:
                    create_checkin = False

            if(create_checkin):
                emp_chkn = frappe.new_doc('Employee Checkin')
                emp_chkn.employee = employee
                emp_chkn.device_id = frappe.db.get_value('Employee Checkin Without Log Type', date_wise_checkin[dates][i][0], 'device_id')
                emp_chkn.time = date_wise_checkin[dates][i][1]
                emp_chkn.log_type = log_type
                try:
                    emp_chkn.save()
                except:
                    pass
                log = not(log)

@frappe.whitelist()
def create_employee_checkin(from_date = None, to_date = None):
    if from_date == None:
        from_date = str(date.today() - timedelta(days = 1))

    else:
        from_date = str(from_date)

    if to_date == None:
        to_date = str(date.today())

    else:
        to_date = str(to_date)

    employees = frappe.db.get_all('Employee Checkin Without Log Type', filters={'time': ['between', (from_date, to_date)]}, pluck='employee')
    employees = list(set(employees))

    buffer_time, reset_time = get_ukm_settings()
    
    for employee in employees:
        date_wise_checkin = frappe._dict()
        date_wise_checkin = get_between_dates(date_wise_checkin, from_date, to_date)
        date_wise_checkin = get_datewise_checkins_of_employee(date_wise_checkin, employee, reset_time)
        # date_wise_checkin = validate_with_buffer_time(date_wise_checkin, buffer_time)
        create_employee_checkins(date_wise_checkin, employee, buffer_time)

    scheduler_for_employee_shift()
