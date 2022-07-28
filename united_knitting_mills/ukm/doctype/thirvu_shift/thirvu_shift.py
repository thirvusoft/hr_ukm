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
		employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type','name'],filters={"employee": employee,'attendance':('is', 'not set')},order_by="time")
		shift_list = frappe.get_doc('Thirvu Shift',{'name':doc})
		row = frappe._dict()
		checkin = frappe._dict()
		for data in employee_checkin:
			validate_time = shift_list.thirvu_shift_details[0].start_time - datetime.timedelta(hours = 1)
			if data.time.date() in row:
				add_values_to_key(row,data.time.date(),[data])
				add_values_to_key(checkin,data.time.date(),[data['name']])

			else:
				if to_timedelta(str(data.time.time())) < validate_time:
					add_values_to_key(row,data.time.date() - datetime.timedelta(days = 1),[data])
					add_values_to_key(checkin,data.time.date() - datetime.timedelta(days = 1),[data['name']])
				else:
					row.update({data.time.date():[data]})
					checkin.update({data.time.date():[data['name']]})

		for value in row:
			start_time = 0
			end_time = 0
			start = 0
			end = 0
			details = []
			approval_details=[]
			attendance_doc = frappe.new_doc('Attendance')
			total_shift_hour = 0
			total_shift_count =0
			attendance_doc.employee = employee
			attendance_doc.attendance_date = value
		
			single_row = frappe._dict()
			for data in row[value]:
				if data['log_type']=='IN':
					start_time = data['time'].time()
					shift_start_time = data['time']
					start = 1

				if data['log_type'] == 'OUT':
					end_time = data['time'].time()
					shift_end_time = data['time']
					end = 1


				if start and end:
					single_row = frappe._dict()
					for data in shift_list.thirvu_shift_details:
						before_start_time = data.start_time - datetime.timedelta(hours = 1)
						after_start_time = data.start_time + datetime.timedelta(minutes = json.loads(late_entry))
						before_end_time = data.end_time - datetime.timedelta(minutes = json.loads(early_exit))
						after_end_time = data.end_time + datetime.timedelta(minutes = 15)

						if  to_timedelta(str(start_time)) >= before_start_time and to_timedelta(str(start_time)) <= after_start_time:
							single_row.update({'start_time':start_time})
							start = 0
							
						else:
							approval_start_time = start_time
						
						if to_timedelta(str(end_time)) >= before_end_time and to_timedelta(str(end_time)) <= after_end_time:
							single_row.update({'end_time':end_time})
							end = 0
							print(single_row)
							
						else:
							approval_end_time = end_time

						print(single_row)
						if(len(single_row.keys()) == 2):
							shift_hours =  shift_end_time - shift_start_time
							single_row.update({'shift_hours':  shift_hours / datetime.timedelta(hours=1),'shift_count':data.shift_count,'shift_status':data.shift_status})
							details.append(single_row)
							total_shift_hour += single_row['shift_hours']
							total_shift_count += data.shift_count
							break

						try:
							if single_row['start_time']:
								approval_row = frappe._dict()
								approval_row.update({'check_in_time':single_row['start_time'],'check_out_time':approval_end_time})
								approval_details.append(approval_row)
								start = 0
								end = 0
								break
						except:
							pass
						try:
							if single_row['end_time']:
								approval_row = frappe._dict()
								approval_row.update({'check_in_time':approval_start_time,'check_out_time':single_row['end_time'],})
								approval_details.append(approval_row)
								start = 0
								end = 0
								break
						except:
							pass

			
			if start:
				approval_row = frappe._dict()
				approval_row.update({'check_in_time':start_time,'check_out_time':''})
				approval_details.append(approval_row)
			
			elif end:
				approval_row = frappe._dict()
				approval_row.update({'check_out_time':end_time,'check_in_time':''})
				approval_details.append(approval_row)

			attendance_doc.update({
				'thirvu_shift_details':details,
				'total_shift_hr':total_shift_hour,
				'employee_shift_details':approval_details,
				'total_shift_count':total_shift_count
			})
			
			attendance_doc.insert()
			
			frappe.db.sql("""update `tabEmployee Checkin`
				set attendance = %s
				where name in %s""", (attendance_doc.name , checkin[value]))
		
			if not attendance_doc.employee_shift_details:
				attendance_doc.submit()

					
def add_values_to_key(temp_dict, key, list_of_values):
    if key not in temp_dict:
        temp_dict[key] = list()
    temp_dict[key].extend(list_of_values)
    return temp_dict