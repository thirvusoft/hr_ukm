# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
import json
import itertools
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, getdate, to_timedelta
import datetime


class ThirvuShift(Document):
	pass 

@frappe.whitelist()
def create_employee_attendance(departments,doc,late_entry,early_exit):
	# To get employee only foe the particular department
	total_employees=frappe.db.get_list('Employee', {"department":departments})
	for employee_details in total_employees:
		employee=employee_details["name"]
		# To Get Employee CheckIn Details
		employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type','name'],filters={"employee": employee,'attendance':('is', 'not set')},order_by="time")
		# To Get Shift Details
		shift_list = frappe.get_doc('Thirvu Shift',{'name':doc})
		#  To Separate The Checkin Date-wise and Getting That Checkin Name
		if shift_list.thirvu_shift_details:
			validate_time = shift_list.thirvu_shift_details[0].start_time - datetime.timedelta(hours = 1)
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
				checkin_type_in = 0
				checkin_type_out = 0
				correct_shift_details = []
				approval_details=[]
				new_attendance_doc = frappe.new_doc('Attendance')
				total_shift_hour = 0
				total_shift_count =0
				new_attendance_doc.employee = employee
				new_attendance_doc.attendance_date = date
			
				# finalattendance = frappe._dict()

				# To Separate the In and Out Time
				for checking_details in date_wise_checkin[date]:
					# For In-Time
					if checking_details['log_type']=='IN':
						in_time = checking_details['time'].time()
						in_time_date = checking_details['time']
						checkin_type_in = 1
					# For Out-Time
					if checking_details['log_type'] == 'OUT':
						out_time = checking_details['time'].time()
						out_time_date = checking_details['time']
						checkin_type_out = 1

					# Caculating Attendance 
					if checkin_type_in and checkin_type_out:
						shift_wise_details = frappe._dict()
						# Calculating Shift
						for shift_details in shift_list.thirvu_shift_details:
							# Checking Buffer Time
							buffer_before_start_time = shift_details.start_time - datetime.timedelta(hours = 1)
							buffer_after_start_time = shift_details.start_time + datetime.timedelta(minutes = json.loads(late_entry))
							buffer_before_end_time = shift_details.end_time - datetime.timedelta(minutes = json.loads(early_exit))
							buffer_after_end_time = shift_details.end_time + datetime.timedelta(minutes = 15)
							# Buffer calculation for starting time
							if  to_timedelta(str(in_time)) >= buffer_before_start_time and to_timedelta(str(in_time)) <= buffer_after_start_time:
								shift_wise_details.update({'start_time':in_time})
								checkin_type_in = 0
								
							else:
								approval_start_time = in_time
							# Buffer calculation for ending time
							if to_timedelta(str(out_time)) >= buffer_before_end_time and to_timedelta(str(out_time)) <= buffer_after_end_time:
								shift_wise_details.update({'end_time':out_time})
								checkin_type_out = 0
								
							else:
								approval_end_time = out_time

							if(len(shift_wise_details.keys()) == 2):
								worked_shift_hours =  out_time_date - in_time_date
								shift_wise_details.update({'shift_hours':  worked_shift_hours / datetime.timedelta(hours=1),'shift_count':shift_details.shift_count,'shift_status':shift_details.shift_status})
								correct_shift_details.append(shift_wise_details)
								total_shift_hour += shift_wise_details['shift_hours']
								total_shift_count += shift_details.shift_count
								break
							try:
								if shift_wise_details['start_time']:
									assigned_shift_hours = shift_details.shift_hours/2
									worked_shift_hours = (out_time_date - in_time_date) / datetime.timedelta(hours=1)
									if worked_shift_hours >= assigned_shift_hours and worked_shift_hours < shift_details.shift_hours:
										shift_wise_details.update({'end_time':approval_end_time,'shift_hours':worked_shift_hours,'shift_count':shift_details.shift_count / 2,'shift_status':shift_details.shift_status})
										new_attendance_doc.early_exit = 1
										correct_shift_details.append(shift_wise_details)
									elif worked_shift_hours > assigned_shift_hours and worked_shift_hours > shift_details.shift_hours :
										approval_timing = frappe._dict()
										approval_timing.update({'check_out_time':approval_end_time,'check_in_time':shift_wise_details['start_time']})
										approval_details.append(approval_timing)
									else:
										shift_wise_details.update({'end_time':approval_end_time,'shift_hours':worked_shift_hours,'shift_count':0.0 ,'shift_status':shift_details.shift_status})
										new_attendance_doc.early_exit = 1
										correct_shift_details.append(shift_wise_details)
									checkin_type_in = 0
									checkin_type_out = 0
									break
							except:
								pass
							try:
								if shift_wise_details['end_time']:
									assigned_shift_hours = shift_details.shift_hours/2
									worked_shift_hours = (out_time_date - in_time_date) / datetime.timedelta(hours=1)
									
									if worked_shift_hours > assigned_shift_hours and worked_shift_hours < shift_details.shift_hours:
										shift_wise_details.update({'start_time':approval_start_time,'shift_hours':worked_shift_hours,'shift_count':shift_details.shift_count / 2,'shift_status':shift_details.shift_status})
										new_attendance_doc.late_entry = 1
										correct_shift_details.append(shift_wise_details)
									elif worked_shift_hours > assigned_shift_hours and worked_shift_hours > shift_details.shift_hours :
										approval_timing = frappe._dict()
										approval_timing.update({'check_out_time':shift_wise_details['end_time'],'check_in_time':approval_start_time})
										approval_details.append(approval_timing)
									else:
										shift_wise_details.update({'start_time':approval_start_time,'shift_hours':worked_shift_hours,'shift_count':0.0,'shift_status':shift_details.shift_status})
										new_attendance_doc.late_entry = 1
										correct_shift_details.append(shift_wise_details)
									checkin_type_in = 0
									checkin_type_out = 0
									break
							except:
								pass
							# If both checkin time and checkout time are wrong
							if checkin_type_in and checkin_type_out:
								approval_timing = frappe._dict()
								approval_timing.update({'check_out_time':out_time,'check_in_time':in_time})
								approval_details.append(approval_timing)
								checkin_type_in = 0
								checkin_type_out = 0
								break

				if checkin_type_in:
					approval_timing = frappe._dict()
					approval_timing.update({'check_in_time':in_time,'check_out_time':''})
					approval_details.append(approval_timing)
				
				elif checkin_type_out:
					approval_timing = frappe._dict()
					approval_timing.update({'check_out_time':out_time,'check_in_time':''})
					approval_details.append(approval_timing)

				# To create attendance document
				new_attendance_doc.update({
					'thirvu_shift_details':correct_shift_details,
					'total_shift_hr':total_shift_hour,
					'employee_shift_details':approval_details,
					'total_shift_count':total_shift_count
				})
				new_attendance_doc.insert()
				
				# To update attendance name in employee checkin
				frappe.db.sql("""update `tabEmployee Checkin`
					set attendance = %s
					where name in %s""", (new_attendance_doc.name , checkin_name[date]))

				# If all shift details are correct it will submit automatically
				if not new_attendance_doc.employee_shift_details:
					new_attendance_doc.submit()

					
def adding_checkin_datewise(checkin_date, checkin_date_key, checkin_details):
    if checkin_date_key not in checkin_date:
        checkin_date[checkin_date_key] = list()
    checkin_date[checkin_date_key].extend(checkin_details)
    # return temp_dict