# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
				frappe.throw("For HR Manager User : "+hr_user["name"]+" there is no Employee ID")
	else:
		frappe.throw("HR Manager role not assigned for any User")




