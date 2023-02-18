# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
<<<<<<< Gokulnath_dev
=======
from frappe import _
from frappe.utils import getdate, nowdate
from datetime import date, datetime, timedelta

>>>>>>> local

class UnitedKnittingMillsSettings(Document):
	pass

@frappe.whitelist()
def creating_hr_permission():
	ts_hr_user=frappe.get_all("User",filters={"role_profile_name":"HR Manager"},fields=["name"])
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
									ts_emp.save()
					else:
						frappe.throw("For HR Manager : "+ts_hr_emp+" Location not set...")
			else:
<<<<<<< Gokulnath_dev
				frappe.throw("For HR Manager User : "+hr_user["name"]+" there is no Employee ID")
	else:
		frappe.throw("HR Manager role not assigned for any User")
=======
				frappe.throw("For Thirvu HR User : "+hr_user["name"]+" there is no Employee ID")
	else:
		frappe.throw("Thirvu HR User role not assigned for any User")

@frappe.whitelist()
def re_create_attendance(attendance_date, employee = None):

	attendance_date = getdate(attendance_date)

	if attendance_date < getdate(nowdate()):

		frappe.msgprint("Within 30 Minutes Attendance Will Be Re-Created.")
		data = []
		data.append(attendance_date)
		data.append(employee)

		frappe.enqueue(attendance_update, data = data, queue = "long")

	else:
		frappe.throw("Date Should Not Be Greater Than Yesterday",title=_("Message"))

def attendance_update(data):

	attendance_list = frappe.get_all("Attendance",{"attendance_date":data[0], "employee":data[1]})

	for attendance in attendance_list:

		attendance_doc = frappe.get_doc("Attendance",attendance)

		if attendance_doc.docstatus:

			attendance_doc.cancel()
			
		try:
			frappe.delete_doc("Attendance Shift Changes", attendance_doc.name)

		except:
			pass

		frappe.delete_doc('Attendance', attendance_doc.name)

	reset_time = frappe.db.get_single_value('United Knitting Mills Settings', 'checkin_type_resetting_time')
	reset_time = datetime.strptime(str(reset_time),'%H:%M:%S')

	start_date = datetime.combine(data[0], reset_time.time())
	end_date = datetime.combine(data[0] + timedelta(days = 1), reset_time.time())

	employee_checkin_list = frappe.get_all("Employee Checkin",{"time":["between",(start_date, end_date)], "employee": data[1]})
>>>>>>> local




<<<<<<< Gokulnath_dev
=======
	create_employee_checkin(data[0], data[0])
>>>>>>> local
