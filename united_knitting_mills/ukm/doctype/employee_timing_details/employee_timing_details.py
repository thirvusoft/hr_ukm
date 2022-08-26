# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
import json
import itertools
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, getdate, to_timedelta, time_diff_in_hours
import datetime
from frappe import _
from datetime import datetime as dt, timedelta

class EmployeeTimingDetails(Document):
	def validate(self):
		self.validate_staff_or_labour()
		self.validate_break_time()
		if(self.staff):
			self.validate_total_checkin()
			self.validate_working_hours()

	def validate_staff_or_labour(self):
		if(not self.staff and not self.labour):
			frappe.throw("Please Select <b>Staff</b> or <b>Labour</b>")

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

	def validate_working_hours(self):
		break_time = self.validate_break_time() * 60
		working_hours = dt.strptime(self.no_working_hours_per_day, '%H:%M:%S').time()
		working_hours_list = str(working_hours).split(':')
		working_hours_delta = timedelta(hours=int(working_hours_list[0]), minutes=int(working_hours_list[1]), seconds=int(working_hours_list[2]))
		working_minutes = working_hours_delta.total_seconds() / 60
		if(break_time >= working_minutes):
			frappe.throw('No of Working Hours Per day should be greater than Total Break Hours')

def get_employees_for_shift(doc, location):
	# To get designation List
	designation = frappe.db.get_list('Designation',{'thirvu_shift':doc, 'name':['!=', 'LINE SUPERISOR']},pluck='name')

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
					WHERE ssa.employee = '{0}' ORDER BY ssa.creation DESC LIMIT 1
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
				correct_shift_details = []
				approval_details=[]
				new_attendance_doc = frappe.new_doc('Attendance')
				new_attendance_doc.employee = employee
				new_attendance_doc.attendance_date = date
				# finalattendance = frappe._dict()
				
				# To check missing log
				if len(date_wise_checkin[date])%2 ==0 and len(date_wise_checkin[date]) :
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
						buffer_before_start_time = shift_details.start_time - datetime.timedelta(hours = 1)
						buffer_after_start_time = shift_details.start_time + datetime.timedelta(minutes = json.loads(late_entry))
						buffer_before_end_time = shift_details.end_time - datetime.timedelta(minutes = json.loads(early_exit))
						if shift_details.idx < len(shift_list.thirvu_shift_details):
							buffer_after_end_time = shift_list.thirvu_shift_details[shift_details.idx].end_time
						else:	
							buffer_after_end_time = shift_list.thirvu_shift_details[shift_details.idx - 1].end_time + datetime.timedelta(hours = 1)

						# Buffer calculation for starting time
						if  in_time and to_timedelta(str(in_time)) >= buffer_before_start_time and to_timedelta(str(in_time)) <= buffer_after_start_time:
							shift_wise_details.update({'start_time':in_time})
							start_idx = shift_details.idx
						else:
							approval_start_time = in_time

						# Buffer calculation for end time
						if out_time and to_timedelta(str(out_time)) >= buffer_before_end_time and to_timedelta(str(out_time)) < buffer_after_end_time:
							shift_wise_details.update({'end_time':out_time})
							end_idx = shift_details.idx
						else:
							approval_end_time = out_time 
							
					# Calculation of shift salary and shift count
					try:
						if start_idx and end_idx:
							shift_count = 0
							shift_salary = 0
							for shift_row in shift_list.thirvu_shift_details:
								if shift_row.idx >= start_idx and shift_row.idx <= end_idx:
									shift_count += shift_row.shift_count
									if frappe.db.get_value('Thirvu Shift Status',shift_row.shift_status,'double_salary'):
										shift_salary += emp_base_amount * ( shift_row.shift_count * 2 )

									else:
										shift_salary += emp_base_amount * ( shift_row.shift_count )

							shift_wise_details.update({'shift_count':shift_count,'shift_salary':shift_salary})
							correct_shift_details.append(shift_wise_details)

					except:
						try:
							if shift_wise_details['start_time'] and approval_end_time:
								approval_timing = frappe._dict()
								approval_timing.update({'check_out_time':approval_end_time,'check_in_time':shift_wise_details['start_time']})
								approval_details.append(approval_timing)

						except:
							if shift_wise_details['end_time'] and approval_start_time:
								approval_timing = frappe._dict()
								approval_timing.update({'check_out_time':shift_wise_details['end_time'],'check_in_time':approval_start_time})
								approval_details.append(approval_timing)
						
					new_attendance_doc.update({
						'thirvu_shift_details':correct_shift_details,
						'employee_shift_details':approval_details,
					})
					new_attendance_doc.insert()
					
				# To create approval for missing entry
				else:
					approval_timing = frappe._dict()
					approval_timing.update({'check_in_time':date_wise_checkin[date][0]['time'].time(),'check_out_time':''})

					approval_details.append(approval_timing)
					new_attendance_doc.update({
						'employee_shift_details':approval_details
					})
					new_attendance_doc.insert()
				
				# Link the Attendance
				frappe.db.sql("""update `tabEmployee Checkin`
					set attendance = %s
					where name in %s""", (new_attendance_doc.name , checkin_name[date]))

				# If all shift details are correct it will submit automatically
				if not new_attendance_doc.employee_shift_details and new_attendance_doc.thirvu_shift_details:
					new_attendance_doc.submit()

def adding_checkin_datewise(checkin_date, checkin_date_key, checkin_details):
    if checkin_date_key not in checkin_date:
        checkin_date[checkin_date_key] = list()
    checkin_date[checkin_date_key].extend(checkin_details)
    # return temp_dict

def get_date_wise_checkin_for_staff(emp_checkins, date_wise_checkin):
	"""Generate a dictionary with date wise checkins of employee"""
	for checkin in emp_checkins:
		if(checkin['time'].date() not in date_wise_checkin):
			date_wise_checkin[checkin['time'].date()] = []
	for checkin in emp_checkins:
		date_wise_checkin[checkin['time'].date()].append(checkin)

def create_datewise_attendance_for_staff(submit_doc, employee, attendance, date, checkins):
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
		submit_doc=False
	if(checkins[-1]['log_type'] == 'OUT'):
		thirvu_shift_details[0].update({
			'end_time': checkins[-1]['time'].time()
		})
	else:
		submit_doc=False
	attendance.update({
		'thirvu_shift_details' : thirvu_shift_details
	})
	return submit_doc

def check_break_time_checkins_for_staff(att_name, doc, submit_doc, times):
	"""Validate Break Time Consumed with Checkins Related to that time
	   Conditions for IN: Except First IN all In time should be less than or equal to brake end time.
	   Conditions for OUT: Except Last OUT all out time should be greater than or equal to break start time.
	   Times variable consists lists of list times eg. [[in_time, out_time], [in_time, out_time]].
	"""
	comment = False
	checkin_list = []
	if(len(times)>1):
		for i in range(0, len(times)):
			for brk_time in doc.break_time:
				# Check In Logs
				if(i != 0):
					if not(times[i][0] <= dt.strptime(str(brk_time.end_time), '%H:%M:%S').time()):
						submit_doc = False
						comment = True
						checkin_list.append(str(times[i][0]))
						frappe.errprint(times[i][0])
				# Check Out Logs
				if(i != (len(times)-1)):
					if not(times[i][1] >= dt.strptime(str(brk_time.start_time), '%H:%M:%S').time()):
						submit_doc = False
						comment = True
						checkin_list.append(str(times[i][1]))
					
	if(comment):
		cmt = frappe.new_doc('Comment')
		cmt.comment_type = 'Comment'
		cmt.reference_doctype = 'Attendance'
		cmt.reference_name = att_name
		cmt.content = f"<p>Break Time Over Consumed.<p><p>For Checkins: {', '.join(checkin_list)}"
		cmt.insert()
	return submit_doc

def validate_total_working_hours(doc, submit_doc, hours_to_work, checkins, attendance):
	"""Validate Total Worked Hours and Break Time"""
	if(len(checkins)%2 == 1):
		submit_doc=False
		return 
	if(not attendance.thirvu_shift_details[0].get('start_time') or not attendance.thirvu_shift_details[0].get('end_time')):
		submit_doc = False
		return
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
		
		submit_doc = check_break_time_checkins_for_staff(attendance.name, doc, submit_doc, times)
		for time in times:
			if(len(time) == 2):
				worked_time += time_diff_in_hours(str(time[1]), str(time[0]))
		
		working_hours = dt.strptime(str(hours_to_work), '%H:%M:%S').time()
		working_hours_list = str(working_hours).split(':')
		working_hours_delta = timedelta(hours=int(working_hours_list[0]), minutes=int(working_hours_list[1]), seconds=int(working_hours_list[2]))
		working_hours = working_hours_delta.total_seconds() / (60*60)
		attendance.thirvu_shift_details[0].update({
			'shift_count':1,
			'shift_hours':worked_time
		})
		attendance.total_shift_count = 1
		attendance.total_shift_hr = worked_time*60
		emp_base_amount=frappe.db.sql("""select ssa.base
					FROM `tabSalary Structure Assignment` as ssa
					WHERE ssa.employee = '{0}' and ssa.docstatus = 1 ORDER BY ssa.creation DESC LIMIT 1
					""".format(attendance.employee),as_list=1)
		if(emp_base_amount):
			emp_base_amount = emp_base_amount[0][0]
		else:
			emp_base_amount=0
		attendance.total_shift_amount = emp_base_amount
		if(worked_time <working_hours):
			submit_doc = False
			attendance.insufficient_hours = 1
		return submit_doc

@frappe.whitelist()
def create_staff_attendance(docname):
	"""Staff Attendance"""
	doc = frappe.get_doc("Employee Timing Details", docname)
	employee_list = get_employees_for_shift(docname, doc.unit)
	
	for employee in employee_list:
		submit_doc = True
		date_wise_checkin = frappe._dict()
		emp_checkins = frappe.db.get_all("Employee Checkin", 
			filters={"employee": employee,'attendance':('is', 'not set')}, 
			order_by="time",
			fields=['time', 'log_type', 'name']
			)
		#Get checkin for this employee
		get_date_wise_checkin_for_staff(emp_checkins, date_wise_checkin)
		for data in date_wise_checkin:
			if(len(date_wise_checkin[data]) < doc.total_no_of_checkins_per_day): submit_doc = False
			attendance = frappe.new_doc('Attendance')
			submit_doc = create_datewise_attendance_for_staff(submit_doc, employee, attendance, data, date_wise_checkin[data])
			submit_doc = validate_total_working_hours(doc, submit_doc, doc.no_working_hours_per_day, date_wise_checkin[data], attendance)
			attendance.flags.ignore_validate = True
			attendance.save()
			if(submit_doc):
				attendance.submit()
