# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
import itertools
from frappe.model.document import Document
from erpnext.hr.doctype.shift_type.shift_type import ShiftType
class ThirvuShift(Document):
	pass

@frappe.whitelist()
def create_employee_attendance(employee,doc):
		employee_checkin = frappe.db.get_list('Employee Checkin',fields=["time",'log_type'],filters={"employee": employee},order_by="time")

		row = frappe._dict()
		for data in employee_checkin:
			if data.time.date() in row:
				add_values_to_key(row,data.time.date(),[data])
			else:
				row.update({data.time.date():[data]})
		
		for value in row:
			details = []
			attendance_doc = frappe.new_doc('Attendance')
			attendance_doc.employee = employee
			attendance_doc.attendance_date = value
			shift_details = frappe.db.get_value('Thirvu Shift',doc,'name')
			# print(row[value])

			single_row = frappe._dict()
			for data in row[value]:
				if(data['log_type']=='IN'):
					single_row.update({'start_time':data['time'].time()})
				else:
					single_row.update({'end_time':data['time'].time()})

				if(len(single_row.keys()) == 2):
					details.append(single_row)
					single_row=frappe._dict()


			print(details)
			attendance_doc.update({
				'thirvu_shift_details':details
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