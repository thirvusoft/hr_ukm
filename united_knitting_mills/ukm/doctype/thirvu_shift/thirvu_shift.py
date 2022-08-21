# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
import json
import itertools
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, getdate, to_timedelta
import datetime
from frappe import _

class ThirvuShift(Document):
	pass 

@frappe.whitelist()
def create_employee_attendance(departments,doc,location,late_entry,early_exit):
	# To get designation List
	designation = frappe.db.get_list('Designation',{'thirvu_shift':doc},pluck='name')

	# To get employee only foe the particular department
	total_employees=frappe.db.get_list('Employee', {"designation":['in', designation],'location':location,'status':'Active'})

	for employee_details in total_employees:
		employee=employee_details["name"]
		# To Get Employee CheckIn Details
		employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type','name'],filters={"employee": employee,'attendance':('is', 'not set')},order_by="time")
		# To Get Shift Details
		shift_list = frappe.get_doc('Thirvu Shift',{'name':doc})
		
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
							buffer_after_end_time = shift_list.thirvu_shift_details[shift_details.idx - 1].end_time

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