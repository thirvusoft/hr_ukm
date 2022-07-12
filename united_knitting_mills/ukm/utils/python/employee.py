import frappe
@frappe.whitelist()
def creating_hr_permission(doc):
	ts_emp_doc=frappe.get_doc("Employee",doc)
	ts_hr_user=frappe.get_all("User",filters={"role_profile_name":"HR Manager"},fields=["name"])
	if ts_hr_user:
		ts_count=0
		for hr_user in ts_hr_user:
			ts_hr_user_emp=frappe.get_all("Employee",filters={"user_id":hr_user["name"],"location":ts_emp_doc.location},fields=["user_id"])
			if ts_hr_user_emp:
				ts_user_id=ts_hr_user_emp[0]["user_id"]
				if ts_emp_doc.hr_permission != 1:
					new_user_permission=frappe.get_doc({
						"doctype": "User Permission",
						"user":ts_user_id,
						"allow":"Employee",
						"for_value":ts_emp_doc.name,
						"apply_to_all_doctypes":1
					})
					new_user_permission.save()
					ts_emp_doc.hr_permission=1
					ts_emp_doc.save()
					ts_count=1
					return 0
				else:
					ts_count=1
					return 1
		if ts_count==0:
			frappe.throw("For HR Manager's there is no Employee ID or Location")
	else:
		frappe.throw("HR Manager role not assigned for any User")

def sequence_user_id(doc,event):
	try:
		if doc.__islocal == 1 :
			last_doc = frappe.get_last_doc("Employee", {"location": doc.location})
			doc.attendance_device_id = int(last_doc.attendance_device_id) + 1
	except:
		pass