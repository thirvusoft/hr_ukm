# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

from email.mime import application
import frappe
import json
import itertools
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, getdate, to_timedelta, time_diff_in_hours
import datetime
from frappe import _
import calendar
from datetime import datetime as dt, date, timedelta, time as t

from frappe.utils.data import today,add_days

class EmployeeTimingDetails(Document):
    def validate(self):
        self.validate_staff_or_labour()
        self.validate_break_time()
        if(self.staff):
            self.validate_total_checkin()

    def validate_staff_or_labour(self):
        if(not self.staff and not self.labour and not self.house_keeping):
            frappe.throw("Please Select <b>Staff</b> or <b>Labour</b> or <b>House Keeping</b>")

    def validate_total_checkin(self):
        if(self.total_no_of_checkins_per_day % 2 ==1):
            frappe.throw("Total No of Checkins must be in Even Number.")

    def validate_break_time(self):
        diff_hrs = 0
        for row in self.break_time:
            if(row.start_time >= row.end_time):
                frappe.throw(f'Row #{row.idx}: Start Time cannot be greater than End Time')
            diff_hrs += time_diff_in_hours(row.end_time, row.start_time)
        self.total_break_time_mins = diff_hrs*60
        return diff_hrs

def get_employees_for_shift(doc, location):
    # To get designation List
    designation = frappe.db.get_list('Designation',{'thirvu_shift':doc},pluck='name')

    # To get employee only foe the particular department
    total_employees=frappe.db.get_all('Employee', filters={"designation":['in', designation],'location':location,'status':'Active'}, pluck='name')
    return total_employees


@frappe.whitelist()
def create_labour_attendance(departments,doc,location,late_entry,early_exit):
    total_employees = get_employees_for_shift(doc, location)
    for employee in total_employees:
        # To Get Employee CheckIn Details
        employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type','name'],filters={"employee": employee,'attendance':('is', 'not set')},order_by="time")
        # To Get Shift Details
        shift_list = frappe.get_doc('Employee Timing Details',doc)
        # Shift Salary
        employee_name = employee
        emp_base_amount=frappe.db.sql("""select ssa.base
                    FROM `tabSalary Structure Assignment` as ssa
                    WHERE ssa.employee = '{0}' and ssa.docstatus = 1 ORDER BY ssa.creation DESC LIMIT 1
                    """.format(employee_name),as_list=1)
        if emp_base_amount:
            emp_base_amount = emp_base_amount[0][0]
        else:
            emp_base_amount = 0

        #  To Separate The Checkin Date-wise and Getting That Checkin Name
        if shift_list.thirvu_shift_details:
            validate_time = frappe.db.get_single_value("United Knitting Mills Settings", "checkin_type_resetting_time")
            date_wise_checkin = frappe._dict()
            checkin_name = frappe._dict()
            for data in employee_checkin:
                if data.time.date() in date_wise_checkin:
                    adding_checkin_datewise(date_wise_checkin,data.time.date(),[data])
                    adding_checkin_datewise(checkin_name,data.time.date(),[data['name']])
                else:
                    if to_timedelta(str(data.time.time())) < validate_time:
                        adding_checkin_datewise(date_wise_checkin,data.time.date() - datetime.timedelta(days = 1),[data])
                        adding_checkin_datewise(checkin_name,data.time.date() - datetime.timedelta(days = 1),[data['name']])
                    else:
                        date_wise_checkin.update({data.time.date():[data]})
                        checkin_name.update({data.time.date():[data['name']]})

            # Looping all the checkin details date-wise
            for date in date_wise_checkin:
                in_time = 0
                out_time = 0
                late_entry_time ,early_exit_time = 0 , 0
                correct_shift_details = []
                approval_details=[]
                new_attendance_doc = frappe.new_doc('Attendance')
                new_attendance_doc.staff = 0
                new_attendance_doc.employee = employee
                new_attendance_doc.attendance_date = date
                # finalattendance = frappe._dict()
                if shift_list.labour == 1:
                    new_attendance_doc.labour = 1
                elif shift_list.house_keeping ==1:
                    new_attendance_doc.house_keeping = 1
                # To check missing log
                
                if len(date_wise_checkin[date]) and len(date_wise_checkin[date]) !=1:
                    if len(date_wise_checkin[date])%2 !=0:
                        date_wise_checkin[date].pop(-1)

                    shift_wise_details = frappe._dict()
                    # To Separate the In and Out Time
                    if date_wise_checkin[date][0]['log_type']=='IN':
                        in_time = date_wise_checkin[date][0]['time'].time()
                        in_time_date = date_wise_checkin[date][0]['time']


                    if date_wise_checkin[date][len(date_wise_checkin[date]) - 1]['log_type'] == 'OUT':
                        out_time = date_wise_checkin[date][len(date_wise_checkin[date]) - 1]['time'].time()
                        out_time_date = date_wise_checkin[date][len(date_wise_checkin[date]) - 1]['time']
                    
                    for shift_details in shift_list.thirvu_shift_details:
                        # Checking Buffer Time
                        if shift_details.idx == 1:
                            buffer_before_start_time = shift_list.thirvu_shift_details[0].start_time - datetime.timedelta(hours = 1.5)
                        else:	
                            buffer_before_start_time = shift_list.thirvu_shift_details[shift_details.idx -2].start_time + datetime.timedelta(minutes = json.loads(late_entry))
                            
                        # buffer_before_start_time = shift_details.start_time - datetime.timedelta(hours = 1)
                        buffer_after_start_time = shift_details.start_time + datetime.timedelta(minutes = json.loads(late_entry))
                        if not shift_details.start_time:
                                buffer_after_start_time = datetime.timedelta(hours=24, minutes=0) + datetime.timedelta(minutes = json.loads(late_entry))
                        buffer_before_end_time = shift_details.end_time - datetime.timedelta(minutes = json.loads(early_exit))
                        if not buffer_before_end_time:
                            buffer_before_end_time = datetime.timedelta(hours=24, minutes=0, days = -1)
            
                        if shift_details.idx < len(shift_list.thirvu_shift_details):
                            buffer_after_end_time = shift_list.thirvu_shift_details[shift_details.idx].end_time
                            
                            if not buffer_after_end_time:
                                
                                buffer_after_end_time = datetime.timedelta(hours=24, minutes=0)
                        else:	
                            buffer_after_end_time = shift_list.thirvu_shift_details[shift_details.idx - 1].end_time + datetime.timedelta(hours = 5)
                            if not buffer_after_end_time:
                                buffer_after_end_time = datetime.timedelta(hours=24, minutes=0)
                        # Buffer calculation for starting time
                        if  in_time and to_timedelta(str(in_time)) >= buffer_before_start_time and to_timedelta(str(in_time)) <= buffer_after_start_time:
                            shift_wise_details.update({'start_time':in_time})
                            start_idx = shift_details.idx
                        else:
                            if shift_details.start_time < to_timedelta(str(in_time)) and shift_list.thirvu_shift_details[0].start_time <= shift_details.start_time: 
                                late_entry_time =to_timedelta(str(in_time)) - shift_details.start_time
                            approval_start_time = in_time

                        # Buffer calculation for end time
                        if out_time and to_timedelta(str(out_time)) >= buffer_before_end_time and to_timedelta(str(out_time)) < buffer_after_end_time:
                            shift_wise_details.update({'end_time':out_time})
                            end_idx = shift_details.idx
                        else:
                            if shift_details.end_time > to_timedelta(str(out_time)) and shift_list.thirvu_shift_details[0].start_time >= shift_details.start_time:
                                early_exit_time = shift_details.end_time - to_timedelta(str(out_time))
                            approval_end_time = out_time 
                    # Calculation of shift salary and shift count
                    try:
                        for i in date_wise_checkin:
                            
                            if start_idx and end_idx:
                                shift_count = 0
                                shift_salary = 0
                                for x in range(0,len(date_wise_checkin[i]),2):
                                    check = 0
                                    break_var = 0
                                    for shift_row in shift_list.thirvu_shift_details:

                                        test_start_time=(datetime.datetime.min + shift_row.start_time).time()
                                        test_end_time=(datetime.datetime.min + shift_row.end_time).time()

                                        if shift_row.start_time > frappe.db.get_single_value("United Knitting Mills Settings", "checkin_type_resetting_time"):
                                            start_time = datetime.datetime.combine(date, test_start_time)
                                        else:
                                            start_time = datetime.datetime.combine(add_days(date,1),test_start_time )

                                        if shift_row.end_time > frappe.db.get_single_value("United Knitting Mills Settings", "checkin_type_resetting_time"):
                                            end_time = datetime.datetime.combine(date, test_end_time)
                                        else:
                                            end_time = datetime.datetime.combine(add_days(date,1), test_end_time)


                                        intime=date_wise_checkin[i][x]['time']
                                        outtime= date_wise_checkin[i][x+1]['time']
                                        try:
                                            if x==0:
                                                intime= date_wise_checkin[i][x]['time'] - timedelta(minutes=int(late_entry))
                                            if x==(len(date_wise_checkin[i]) -2):
                                                outtime= date_wise_checkin[i][x+1]['time'] + timedelta(minutes=int(early_exit))
                                        except:
                                            frappe.log_error(frappe.get_traceback())

                                        
                                        if intime < (start_time) and  outtime  > (end_time):
                                            check = 1
                                            shift_count += shift_row.shift_count
                                            if frappe.db.get_value('Thirvu Shift Status',shift_row.shift_status,'double_salary'):
                                                shift_salary += emp_base_amount * ( shift_row.shift_count * 2 )

                                            else:
                                                shift_salary += emp_base_amount * ( shift_row.shift_count )
                                        else:

                                            if check:
                                                break_var = 1
    
                                        if check and break_var:
                                            break

                                shift_wise_details.update({'shift_count':shift_count,'shift_salary':shift_salary})
                                correct_shift_details.append(shift_wise_details)
                                new_attendance_doc.update({
                                    'checkin_time':shift_wise_details['start_time'],                                    
                                    'checkout_time':shift_wise_details['end_time']
                                })

                    except:

                        next = 1
                        new_attendance_doc.update({
                                'checkin_time':'',
                                'checkout_time':''
                            })
                        try:

                            if shift_wise_details['start_time'] and approval_end_time and next:
                                approval_timing = frappe._dict()
                                approval_timing.update({'check_out_time':approval_end_time,'check_in_time':shift_wise_details['start_time']})
                                new_attendance_doc.update({'early_exit':1,'exit_period':early_exit_time /  datetime.timedelta(minutes=1)})
                                approval_details.append(approval_timing)

                                next = 0
                        except:
                            pass

                        try:
                            
                            if shift_wise_details['end_time'] and approval_start_time and next:
                                approval_timing = frappe._dict()
                                approval_timing.update({'check_out_time':shift_wise_details['end_time'],'check_in_time':approval_start_time})
                                new_attendance_doc.update({'late_entry':1,'late_min':late_entry_time /  datetime.timedelta(minutes=1)})
                                approval_details.append(approval_timing)
                                next = 0
                        except:
                            pass
                        
                        try:
                            if approval_start_time and approval_end_time and next:
                                approval_timing = frappe._dict()
                                approval_timing.update({'check_out_time':approval_end_time,'check_in_time':approval_start_time})
                                approval_details.append(approval_timing)

                        except:
                            pass
                        try:
                            if shift_wise_details['end_time'] and approval_start_time and next:
                                approval_timing = frappe._dict()
                                approval_timing.update({'check_out_time':shift_wise_details['end_time'],'check_in_time':approval_start_time})
                                approval_details.append(approval_timing)
                                next = 0
                        except:
                            pass
                        

                    new_attendance_doc.update({
                        'thirvu_shift_details':correct_shift_details,
                        'employee_shift_details':approval_details,
                    })
                    new_attendance_doc.insert()
                    
                # To create approval for missing entry
                else:
                    # approval_timing = frappe._dict()
                    # approval_timing.update({'check_in_time':date_wise_checkin[date][0]['time'].time(),'check_out_time':''})

                    # approval_details.append(approval_timing)
                    # new_attendance_doc.update({
                    #     'employee_shift_details':approval_details
                    # })
                    new_attendance_doc.update({
                                "total_shift_count":0,
                                'mismatched_checkin':1,
                                'no_of_checkin':f"{len(date_wise_checkin[date])}",
                                'checkin_time':'',
                                'checkout_time':''
                            })
                    new_attendance_doc.insert()
                
                # Link the Attendance
                frappe.db.sql("""update `tabEmployee Checkin`
                    set attendance = %s
                    where name in %s""", (new_attendance_doc.name , checkin_name[date]))

                # If all shift details are correct it will submit automatically
                if not new_attendance_doc.employee_shift_details:
                    new_attendance_doc.reload()
                    new_attendance_doc.submit()

def adding_checkin_datewise(checkin_date, checkin_date_key, checkin_details):
    if checkin_date_key not in checkin_date:
        checkin_date[checkin_date_key] = list()
    checkin_date[checkin_date_key].extend(checkin_details)
    # return temp_dict

def get_date_wise_checkin_for_staff(emp_checkins, date_wise_checkin,logs):

    validate_time = frappe.db.get_single_value("United Knitting Mills Settings", "checkin_type_resetting_time")
    for data in emp_checkins:
        if data.time.date() in date_wise_checkin:
            adding_checkin_datewise(date_wise_checkin,data.time.date(),[data])
            adding_checkin_datewise(logs,data.time.date(),[data['name']])
        else:
            if to_timedelta(str(data.time.time())) < validate_time:
                adding_checkin_datewise(date_wise_checkin,data.time.date() - datetime.timedelta(days = 1),[data])
                adding_checkin_datewise(logs,data.time.date() - datetime.timedelta(days = 1),[data['name']])
            else:
                date_wise_checkin.update({data.time.date():[data]})
                logs.update({data.time.date():[data['name']]})


    # """Generate a dictionary with date wise checkins of employee"""
    # for checkin in emp_checkins:
    #     if(checkin['time'].date() not in date_wise_checkin):
    #         date_wise_checkin[checkin['time'].date()] = []
    #         logs[checkin['time'].date()] = []

    # for checkin in emp_checkins:
    #     date_wise_checkin[checkin['time'].date()].append(checkin)
    #     logs[checkin['time'].date()].append(checkin['name'])

def create_datewise_attendance_for_staff(reason, submit_doc, employee, attendance, date, checkins):
    """Fill Attendance doc with start time, end time and other employee details"""
    attendance.employee = employee
    attendance.attendance_date = date
    attendance.department = frappe.db.get_value('Employee', employee, 'department')
    thirvu_shift_details = [{}]
    if(checkins[0]['log_type'] == 'IN'):
        thirvu_shift_details[0].update({
            'start_time': checkins[0]['time'].time()
        })
    else:
        thirvu_shift_details[0].update({
            'start_time': ""
        })
        reason += '\n-> First In Checkin Missing.' 
        attendance.mismatched_checkin = 1
        submit_doc=False
    if(checkins[-1]['log_type'] == 'OUT'):
        thirvu_shift_details[0].update({
            'end_time': checkins[-1]['time'].time()
        })
    else:
        thirvu_shift_details[0].update({
            'end_time': ""
        })
        reason += '\n-> Last Out Checkin Missing.'
        attendance.mismatched_checkin = 1
        submit_doc=False
    attendance.update({
        'thirvu_shift_details' : thirvu_shift_details,
    })
    if attendance.thirvu_shift_details[0].end_time and attendance.thirvu_shift_details[0].start_time:
        attendance.update({
            'checkin_time':attendance.thirvu_shift_details[0].start_time,
            'checkout_time':attendance.thirvu_shift_details[0].end_time
        })
    elif attendance.thirvu_shift_details[0].start_time:
        attendance.update({
            'checkin_time':attendance.thirvu_shift_details[0].start_time,
            'checkout_time':''
        })
    elif attendance.thirvu_shift_details[0].end_time:
        attendance.update({
            'checkin_time':'',
            'checkout_time':attendance.thirvu_shift_details[0].end_time
        })
    else:
        attendance.update({
            'checkin_time':'',
            'checkout_time':''
        })
    return submit_doc, reason

def check_break_time_and_fist_in_last_out_checkins_for_staff(reason, attendance, doc, submit_doc, times, start_time, end_time):
    """Validate Break Time Consumed with Checkins Related to that time
       Conditions for IN: 
            i)  First IN should be less than or equal to start_time.
            ii) Except First IN all In time should be less than or equal to brake end time.
       Conditions for OUT: 
            i)  Last OUT should be greater than or equal to end_time.
            ii) Except Last OUT all out time should be greater than or equal to break start time.
       Times variable consists lists of list times eg. [[in_time, out_time], [in_time, out_time]].
    """
    start_time = list(map(int, str(start_time).split(':')))
    ac_start_time = (dt.combine(date.today(), t(start_time[0], start_time[1], start_time[2]))).time()
    start_time = (dt.combine(date.today(), t(start_time[0], start_time[1], start_time[2]))+ timedelta(minutes=doc.entry_period or 0)).time()
    end_time = list(map(int, str(end_time).split(':')))
    ac_end_time = (dt.combine(date.today(), t(end_time[0], end_time[1], end_time[2]))).time()
    end_time = (dt.combine(date.today(), t(end_time[0], end_time[1], end_time[2]))- timedelta(minutes=doc.exit_period or 0)).time()
    comment = False
    checkin_list = []
    late_entry, early_exit, break_consumed_min, late_entry_min, early_exit_min = 0, 0, 0, 0, 0
    if(len(times)>1):
        # minutes wise breaktime calculation
        out_in_log=[]  #Single List[12, 1, 3, 4]
        out_in_logs=[]  #list of list without first checkin and last checkout [[12, 1], [3, 4]]  out in, out in
        for log in times:
            for i in log:
                out_in_log.append(i)
        #out_in_log = [12, 1, 3, 4]  #original: [[9, 12], [1, 3], [4, 7]]
        temp=[]
        for log in out_in_log[1:-1]:
            if temp:
                temp.append(log)
                out_in_logs.append(temp)
                temp=[]
            else:
                temp=[log]
        #out_in_logs=[[12, 1], [3, 4]]  out in, out in
        break_time=0
        for log in out_in_logs:
            # log -> out, in
            # break_time+=(log[0]-log[1])
                break_time+=(((dt.strptime(str(log[1]), '%H:%M:%S')) - (dt.strptime(str(log[0]), '%H:%M:%S'))) / datetime.timedelta(minutes=1))
        
        # break time calculated
        
        if break_time > doc.total_break_time_mins:
            break_consumed_min=break_time-doc.total_break_time_mins
            submit_doc = False
            comment = True
        else:
            break_consumed_min=0  
            
            # Existing Code
            # for i in range(0, len(times)):
            # for brk_time in doc.break_time:
            #     # Check In Logs
            #     if(i != 0):
            #         if not(times[i][0] <= dt.strptime(str(brk_time.end_time), '%H:%M:%S').time()):
            #             break_consumed_min += (((dt.strptime(str(times[i][0]), '%H:%M:%S')) - (dt.strptime(str(brk_time.end_time), '%H:%M:%S'))) / datetime.timedelta(minutes=1))
            #             submit_doc = False
            #             comment = True
            #             checkin_list.append(str(times[i][0]))
            #     else:
            #         if not(times[i][0] <= dt.strptime(str(start_time), '%H:%M:%S').time()):
            #             late_entry_min += (((dt.strptime(str(times[i][0]), '%H:%M:%S')) - (dt.strptime(str(ac_start_time), '%H:%M:%S'))) / datetime.timedelta(minutes=1))
            #             submit_doc = False
            #             late_entry = 1
            #     # Check Out Logs
            #     if(i != (len(times)-1)):
            #         if not(times[i][1] >= dt.strptime(str(brk_time.start_time), '%H:%M:%S').time()):
            #             submit_doc = False
            #             comment = True
            #             break_consumed_min += (((dt.strptime(str(brk_time.start_time), '%H:%M:%S')) - (dt.strptime(str(times[i][1]), '%H:%M:%S'))) /  datetime.timedelta(minutes=1))
            #             checkin_list.append(str(times[i][1]))
            #     else:
            #         if not(times[i][1] >= dt.strptime(str(end_time), '%H:%M:%S').time()):
            #             submit_doc = False
            #             early_exit_min += (((dt.strptime(str(ac_end_time), '%H:%M:%S')) - (dt.strptime(str(times[i][1]), '%H:%M:%S'))) / datetime.timedelta(minutes=1))
            #             early_exit= 1
    else:        
        if not(times[0][0] <= dt.strptime(str(start_time), '%H:%M:%S').time()):
            submit_doc = False
            late_entry_min += (((dt.strptime(str(times[0][0]), '%H:%M:%S')) - (dt.strptime(str(ac_start_time), '%H:%M:%S'))) /  datetime.timedelta(minutes=1))
            late_entry = 1

        if not(times[0][1] >= dt.strptime(str(end_time), '%H:%M:%S').time()):
            submit_doc = False
            early_exit_min += (((dt.strptime(str(ac_end_time), '%H:%M:%S')) - (dt.strptime(str(times[0][1]), '%H:%M:%S'))) /  datetime.timedelta(minutes=1))
            early_exit= 1

    if late_entry:
        attendance.late_min = late_entry_min
    if early_exit:
        attendance.exit_period = early_exit_min

    if(comment):
        reason +=f"\n-> Break Time Over Consumed for Checkins {', '.join(checkin_list)}"
        attendance.break_time_overconsumed = 1
        attendance.over_consumed_time = break_consumed_min
        cmt = frappe.new_doc('Comment')
        cmt.comment_type = 'Comment'
        cmt.reference_doctype = 'Attendance'
        cmt.reference_name = attendance.name
        cmt.content = f"<p>Break Time Over Consumed.<p><p>For Checkins: {', '.join(checkin_list)}"
        cmt.insert()
    return submit_doc, reason, late_entry, early_exit

def validate_total_working_hours(reason, doc, submit_doc, checkins, attendance, start_time, end_time):
    """Validate Total Worked Hours and Break Time"""
    if(len(checkins)%2 == 1):
        submit_doc=False
        reason += '\n-> Odd number of Checkins Found(IN or Out is Missed)'
        attendance.mismatched_checkin = 1 
        return submit_doc, reason, 0, 0
    if(not attendance.thirvu_shift_details[0].get('start_time') or not attendance.thirvu_shift_details[0].get('end_time')):
        submit_doc = False
        return submit_doc, reason, 0,0
    else:
        times = [[]]
        worked_time=0
        for chkn in checkins:
            if(len(times[-1]) != 2):
                times[-1].append(chkn['time'].time())
            else:
                times.append([chkn['time'].time()])
        attendance.flags.ignore_validate = True
        attendance.insert()
        
        submit_doc, reason, late_entry, early_exit = check_break_time_and_fist_in_last_out_checkins_for_staff(reason, attendance,doc, submit_doc, times, start_time, end_time)
        for time in times:
            if(len(time) == 2):
                # worked_time += time_diff_in_hours(str(time[1]), str(time[0]))

                start_time = str(time[0])
                end_time = str(time[1])
                if(str(type(start_time)) == "<class 'str'>" or str(type(end_time)) == "<class 'str'>"):
                    start_time = str(start_time)
                    end_time = str(end_time)

                if(start_time<=end_time):
                    shift_hr = frappe.db.sql("""select timediff('{0}','{1}') as result""".format(end_time, start_time),as_list = 1)[0][0]
                    shift_hours =  shift_hr / datetime.timedelta(hours=1)
                
                else:
                    shift_hr = frappe.db.sql("""select timediff('{0}','{1}') as result""".format("23:59:59", start_time),as_list = 1)[0][0].__str__()
                    shift_hr = list(map(float, shift_hr.split(':')))
                    end_time = str(end_time).split(':')

                    for i in range(len(end_time)):
                        shift_hr[i]= str(int(shift_hr[i]) + int(float(end_time[i])))

                    delta = datetime.timedelta(hours=int(shift_hr[0]), minutes=int(shift_hr[1]), seconds=int(shift_hr[2]))
                    shift_hours = delta.total_seconds()/ (60*60) 
                    shift_hr = delta

                
                if shift_hours > 0:
                    # if(not data.get('shif_hours')):
                    #     data.shift_hours = shift_hours

                    worked_time += shift_hr / datetime.timedelta(minutes=1)

                else:
                    diff_time = (to_timedelta(str(end_time)) - to_timedelta(str(start_time)))
                    
                    # if not data.get('shif_hours'):
                    #     data.shift_hours = diff_time/ datetime.timedelta(hours=1)
                    
                    worked_time +=  diff_time / datetime.timedelta(minutes=1)
        
        attendance.thirvu_shift_details[0].update({
            'shift_count':1,
            'shift_hours':worked_time
        })
        attendance.total_shift_count = 1
        attendance.total_shift_hr = round(worked_time*60)
        act_work_hrs = calculate_working_hour(doc)
        attendance.ts_ot_hrs = (worked_time - act_work_hrs)*60 if (worked_time >= act_work_hrs) else 0
        emp_base_amount=frappe.db.sql("""select ssa.base
                    FROM `tabSalary Structure Assignment` as ssa
                    WHERE ssa.employee = '{0}' and ssa.docstatus = 1 ORDER BY ssa.creation DESC LIMIT 1
                    """.format(attendance.employee),as_list=1)
        if(emp_base_amount):
            emp_base_amount = emp_base_amount[0][0]
        else:
            emp_base_amount=0
        attendance.total_shift_amount = 0
        if(worked_time <act_work_hrs):
            reason +=f"\n-> Insufficient Working Hours({act_work_hrs} hrs required but only {worked_time} worked)."
            submit_doc = False
            attendance.insufficient_working_minutes = 1
            attendance.insufficient_working_hrs= worked_time
        return submit_doc, reason, late_entry, early_exit

def calculate_working_hour(doc):
    work_time = 0
    work_time += time_diff_in_hours(str(doc.end_time), str(doc.start_time))
    for i in doc.break_time:
        work_time -= time_diff_in_hours(str(i.end_time), str(i.start_time))
    return work_time
reason = ''
@frappe.whitelist()
def create_staff_attendance(docname):
    """Staff Attendance"""
    doc = frappe.get_doc("Employee Timing Details", docname)
    employee_list = get_employees_for_shift(docname, doc.unit)
    for employee in employee_list:
        submit_doc = True
        date_wise_checkin = frappe._dict()
        logs = frappe._dict()
        emp_checkins = frappe.db.get_all("Employee Checkin", 
            filters={"employee": employee,'attendance':('is', 'not set')}, 
            order_by="time",
            fields=['time', 'log_type', 'name']
            )
        #Get checkin for this employee
        get_date_wise_checkin_for_staff(emp_checkins, date_wise_checkin,logs)
        
        holiday_list_name = frappe.db.get_value("Employee", {"name":employee}, "holiday_list")
        holiday_list = frappe.get_doc("Holiday List", holiday_list_name)
        
        holidays = []

        for holiday in holiday_list.holidays:
            holidays.append(holiday.holiday_date)
            
        for data in date_wise_checkin:
            reason = ''
            if(not frappe.db.exists('Attendance', {'attendance_date':data, 'employee':employee})):
                attendance = frappe.new_doc('Attendance')
                if(len(date_wise_checkin[data]) < doc.total_no_of_checkins_per_day):
                    submit_doc = False
                    reason += f"\n-> Insufficient Checkins({doc.total_no_of_checkins_per_day} required but only {len(date_wise_checkin[data])} is available)."
                    attendance.mismatched_checkin = 1
                    attendance.no_of_checkin = f"{len(date_wise_checkin[data])} / { doc.total_no_of_checkins_per_day}"
                attendance.staff = 1
                submit_doc, reason = create_datewise_attendance_for_staff(reason, submit_doc, employee, attendance, data, date_wise_checkin[data])
                submit_doc, reason, late_entry, early_exit = validate_total_working_hours(reason, doc, submit_doc, date_wise_checkin[data], attendance, doc.start_time, doc.end_time)
                attendance.flags.ignore_validate = True
                attendance.late_entry = late_entry
                attendance.early_exit = early_exit
                if(reason != ''):
                    attendance.reason = reason[1::]
                attendance.flags.ignore_validate = True
                attendance.save()
                at_date = getdate(attendance.attendance_date)
                if submit_doc and at_date not in holidays:
                    attendance.reload()
                    attendance.submit()
                else:
                    if at_date in holidays:
                        attendance.sunday_attendance = 1
                    attendance.total_shift_count = 0
                    attendance.save()

                # Link the Attendance
                frappe.db.sql("""update `tabEmployee Checkin`
                    set attendance = %s
                    where name in %s""", (attendance.name , logs[data]))

def scheduler_for_employee_shift(unit=None):
    filters={}
    if unit:
        filters["unit"] = unit
    employee_timing_details = frappe.get_all('Employee Timing Details', filters)
    for data in employee_timing_details:
        timing_doc = frappe.get_doc('Employee Timing Details',data['name'])
        if timing_doc.staff == 1:
            create_staff_attendance(timing_doc.name)
        elif timing_doc.labour ==1 or timing_doc.house_keeping == 1:
            create_labour_attendance(timing_doc.department, timing_doc.name, timing_doc.unit, str(timing_doc.entry_period) ,str(timing_doc.exit_period))
    
    leave_application_to_attendance(unit)
   
def leave_application_to_attendance(unit=None):
    # leave application proccessed to attendance
    filters={"attendance_date": ["<", today()],"docstatus":1,"attendance_marked":0,"leave_type":["in",['On Duty','Permission']]}
    if unit:
        filters["unit"] = unit
    for data in frappe.get_all("Leave Application", filters=filters,pluck='name'):
        application_doc = frappe.get_doc('Leave Application',data)

        if frappe.db.exists('Attendance',{"attendance_date": application_doc.attendance_date,"employee":application_doc.employee,"docstatus":["!=", 2]}):
            existing_doc = frappe.get_doc('Attendance',{"attendance_date": application_doc.attendance_date,"employee":application_doc.employee,"docstatus":["!=", 2]})
            
            if existing_doc.docstatus:

                new_doc = frappe.copy_doc(existing_doc)
                new_doc.workflow_state = "Draft"
                existing_doc.workflow_state = "Cancelled"
                existing_doc.cancel()
                
                new_doc.amended_from = existing_doc.name
                
                new_doc.update({
                    'leave_application': application_doc.name,
                    'leave_type': application_doc.leave_type
                    })
                new_doc.insert()

            else:
                existing_doc.update({
                    'leave_application':application_doc.name,
                    'leave_type':application_doc.leave_type
                    })
                existing_doc.save()
                
            
        else:
            attendance = frappe.new_doc('Attendance')
            attendance.employee = application_doc.employee
            attendance.attendance_date = application_doc.attendance_date
            attendance.leave_application = application_doc.name
            attendance.leave_type = application_doc.leave_type
            attendance.checkin_time = application_doc.from_time
            attendance.checkout_time = application_doc.to_time
            attendance.save()

        application_doc.attendance_marked = 1
        application_doc.save()

