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
				pass
			else:
				row.update({data.time.date():[data]})

		for value in row:
			attendance_doc = frappe.new_doc('Attendance')
			attendance_doc.employee = employee
			attendance_doc.attendance_date = value
			shift_details = frappe.db.get_value('Thirvu Shift',doc,'name')
			row = frappe._dict
			for data in row[value]:
				row.up
				if(data['log_type']=='IN'):
					pass
					# row.update({''})

			for details in shift_details:
				pass
			# attendance_doc.save()

			
def add_values_to_key(temp_dict, key, list_of_values):
    if key not in temp_dict:
        temp_dict[key] = list()
    temp_dict[key].extend(list_of_values)
    return temp_dict