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
def create_employee_attendance(employee,doc,late_entry,early_exit):
		employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type'],filters={"employee": employee},order_by="time")

		row = frappe._dict()
		for data in employee_checkin:
			if data.time.date() in row:
				add_values_to_key(row,data.time.date(),[data])
			else:
				row.update({data.time.date():[data]})
		total_shift_hours = 0
		for value in row:
			details = []
			attendance_doc = frappe.new_doc('Attendance')
			attendance_doc.employee = employee
			attendance_doc.attendance_date = value
			shift_details = frappe.db.get_value('Thirvu Shift',doc,'name')

			single_row = frappe._dict()
			shift_list = frappe.get_doc('Thirvu Shift',{'name':doc})

			if row[value][0]['log_type']=='IN':
				start_time = row[value][0]['time'].time()
				# single_row.update({'start_time':data['time'].time()})

			if row[value][len(row[value]) - 1]['log_type'] == 'OUT':
				frappe.errprint(row[value][len(row[value]) - 1]['time'])
				end_time = row[value][len(row[value]) - 1]['time'].time()

			if start_time and end_time:
				single_row = frappe._dict()
				for data in shift_list.thirvu_shift_details:
					before_start_time = data.start_time - datetime.timedelta(minutes = 15)
					after_start_time = data.start_time + datetime.timedelta(minutes = json.loads(late_entry))
					before_end_time = data.end_time - datetime.timedelta(minutes = json.loads(early_exit))
					after_end_time = data.end_time + datetime.timedelta(minutes = 15)

					frappe.errprint(to_timedelta(str(start_time)))
					frappe.errprint('oookk')
					frappe.errprint(before_start_time)
					frappe.errprint(after_start_time)
					frappe.errprint(to_timedelta(str(end_time)))
					frappe.errprint(before_end_time)
					frappe.errprint(after_end_time)




					if  to_timedelta(str(start_time)) >= before_start_time and to_timedelta(str(start_time)) <= after_start_time:
						single_row.update({'start_time':start_time})
						shift_start_time = start_time
						
					if to_timedelta(str(end_time)) >= before_end_time and to_timedelta(str(end_time)) <= after_end_time:
						single_row.update({'end_time':end_time})
						shift_end_time = end_time
					frappe.errprint(single_row)
					frappe.errprint(len(single_row.keys()))
					if(len(single_row.keys()) == 2):
						frappe.errprint('loop')
						# frappe.errprint(single_row)
						shift_hours =  shift_end_time - shift_start_time
						frappe.errprint(shift_hours)
						single_row.update({'shift_hours':  shift_hours / datetime.timedelta(hours=1)})
						details.append(single_row)
						total_shift_hours += single_row['shift_hours']



				# single_row.update({'end_time':data['time'].time()})

			


			
			attendance_doc.update({
				'thirvu_shift_details':details,
				'total_shift_hours':total_shift_hours
			})
			
			attendance_doc.insert()

			# for time_slot in attendance_doc.thirvu_shift_details:
			# 	shift_duration = frappe.get_doc('Thirvu Shift Details',{'parent':doc})
			# 	for date in shift_duration:
			# 		if time_slot.start_time
					
def add_values_to_key(temp_dict, key, list_of_values):
    if key not in temp_dict:
        temp_dict[key] = list()
    temp_dict[key].extend(list_of_values)
    return temp_dict