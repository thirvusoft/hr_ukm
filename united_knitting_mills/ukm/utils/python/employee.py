import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils.data import get_link_to_form
@frappe.whitelist()
def creating_hr_permission(ts_emp_doc,event):
	ts_hr_user=frappe.get_all("User",filters={"role_profile_name" : "Thirvu HR User"},fields=["name"])
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
					ts_count=1
					return 0
				else:
					ts_count=1
					return 1
		if ts_count==0:
			frappe.throw("For Thirvu HR User there is no Employee ID or Location")
	else:
		frappe.throw("Thirvu HR User role not assigned for any User")

def sequence_user_id(doc,event):
	frappe.db.set_value("Employee",doc.name,"attendance_device_id",doc.name)
	# if doc.approval_by_owner == 1 and doc.status == 'Active':
	# 		doc.status = 'Active'
	# else:
	# 	doc.status = 'Inactive'

def employee_custom_field():
	custom_fields = {
	"Employee": [
		dict(fieldname='employee_naming_series', label='Employee Naming Series',
			fieldtype='Data', insert_after='location',fetch_from="location.naming_series"),
		
	],
    }
	create_custom_fields(custom_fields)
	employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"options",
        'property_type':"Data",
        'field_name':"naming_series",
        "value":"employee_naming_series.-\nUKM-II\nUKM-I"
    })
	employee.save(ignore_permissions=True)
	

def get_employee_shift(employee): 
	"""Requires Employee name as argument"""
	designation = frappe.db.get_value("Employee", employee, 'designation')
	shift = frappe.db.get_value('Designation', designation, 'thirvu_shift')
	if shift: return shift
	designation_url = get_link_to_form('Designation', designation)
	frappe.throw(f'Please Assign Shift for {frappe.bold(designation_url)}.')

def bio_metric_id(doc,event):
	doc.attendance_device_id = doc.name
	doc.save()
	frappe.msgprint("Bio-Metric ID For Employee : <b>"+ doc.employee_name+"</b> Is <b>"+doc.attendance_device_id)