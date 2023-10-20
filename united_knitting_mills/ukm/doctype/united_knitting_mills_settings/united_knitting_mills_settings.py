# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import getdate, nowdate
from datetime import date, datetime, timedelta

from united_knitting_mills.ukm.utils.python.employee__checkin import create_employee_checkin, create_employee_checkin_security
class UnitedKnittingMillsSettings(Document):
	
	def validate(doc):

		for row in doc.advance_amount:

			if row.idx == 1:
				child_table = doc.advance_amount[row.idx - 1].__dict__

			else:
				child_table = doc.advance_amount[row.idx - 2].__dict__
			
			if row.maximum_salary < child_table["maximum_salary"]:

				frappe.throw(f"In Advance, Maximum Salary of Row {row.idx} is Less than Row {row.idx - 1}.",title=_("Message"))


@frappe.whitelist()
def creating_hr_permission():
	ts_hr_user=frappe.get_all("User",filters={"role_profile_name":"Thirvu HR User"},fields=["name"])
	if ts_hr_user:
		for hr_user in ts_hr_user:
			ts_hr_user_emp=frappe.get_all("Employee",filters={"user_id":hr_user["name"]},fields=["name","location","user_id"])
			if ts_hr_user_emp:
				ts_hr_emp=ts_hr_user_emp[0]["name"]
				ts_hr_location=ts_hr_user_emp[0]["location"]
				ts_user_id=ts_hr_user_emp[0]["user_id"]
				if ts_user_id:
					if ts_hr_location:
						ts_user_emp=frappe.get_all("Employee",filters={"location":ts_hr_location},fields=["name"])
						for ts_user_name in ts_user_emp:
							if ts_user_name["name"] != ts_hr_emp:
								ts_emp=frappe.get_doc("Employee",ts_user_name["name"])
								if ts_emp.hr_permission != 1:
									new_user_permission=frappe.get_doc({
										"doctype": "User Permission",
										"user":ts_user_id,
										"allow":"Employee",
										"for_value":ts_emp.name,
										"apply_to_all_doctypes":1
									})
									new_user_permission.save()
									ts_emp.hr_permission=1
					else:
						frappe.throw("For Thirvu HR User : "+ts_hr_emp+" Location not set...")
			else:
				frappe.throw("For Thirvu HR User : "+hr_user["name"]+" there is no Employee ID")
	else:
		frappe.throw("Thirvu HR User role not assigned for any User")

@frappe.whitelist()
def re_create_attendance(attendance_date, employee = None, unit = None):

	attendance_date = getdate(attendance_date)

	if attendance_date < getdate(nowdate()):

		frappe.msgprint("Within 30 Minutes Attendance Will Be Re-Created.")
		data = []
		data.append(attendance_date)
		data.append(employee)

		frappe.enqueue(attendance_update, data = data, unit = unit, queue = "long")

	else:
		frappe.throw("Date Should Not Be Greater Than Yesterday",title=_("Message"))

def attendance_update(data, unit=None):
	filters={"attendance_date":data[0]}
	if data[1]:
		filters["employee"] = data[1]
	if unit:
		filters["unit"] = unit
	attendance_list = frappe.get_all("Attendance",filters)

	count = 0

	for attendance in attendance_list:
		
		count += 1

		attendance_doc = frappe.get_doc("Attendance", attendance)

		attendance_shift_changes = frappe.get_all("Attendance Shift Changes", {"attendance":attendance_doc.name})
		
		for changes in attendance_shift_changes:

			attendance_shift_changes_doc = frappe.get_doc("Attendance Shift Changes", changes)

			if attendance_shift_changes_doc.docstatus == 1:

				attendance_shift_changes_doc.cancel()
				frappe.delete_doc("Attendance Shift Changes", attendance_shift_changes_doc.name)
			
			else:
				frappe.delete_doc("Attendance Shift Changes", attendance_shift_changes_doc.name)


		if attendance_doc.docstatus == 1:
			attendance_doc.cancel()
			frappe.delete_doc('Attendance', attendance_doc.name)

		else:
			frappe.delete_doc('Attendance', attendance_doc.name)



		if count == 100:
			count = 0
			frappe.db.commit()
	shift_det = frappe.db.get_value("Designation",frappe.db.get_value("Employee",data[1],'designation'),'thirvu_shift')
	if not frappe.db.get_value("Employee Timing Details",shift_det,'security_'):
		reset_time = frappe.db.get_single_value('United Knitting Mills Settings', 'checkin_type_resetting_time')
	else:
		reset_time = frappe.db.get_single_value('United Knitting Mills Settings', 'resetting_time_for_security')

	reset_time = datetime.strptime(str(reset_time),'%H:%M:%S')

	start_date = datetime.combine(data[0], reset_time.time())
	end_date = datetime.combine(data[0] + timedelta(days = 1), reset_time.time())
	
	filters = {"time":["between",(start_date, end_date)]}
	if unit:
		filters["unit"] = unit
	if data[1]:
		filters["employee"] = data[1]
	employee_checkin_list = frappe.get_all("Employee Checkin",filters)

	count = 0

	for employee_checkin in employee_checkin_list:

		count += 1

		employee_checkin_doc = frappe.get_doc("Employee Checkin", employee_checkin)

		frappe.delete_doc('Employee Checkin', employee_checkin_doc.name)

		if count == 100:
			count = 0
			frappe.db.commit()

	create_employee_checkin(data[0], data[0], unit)
	create_employee_checkin_security(data[0], data[0], unit)