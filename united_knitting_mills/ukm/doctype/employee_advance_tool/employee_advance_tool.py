import json
import frappe

from frappe.model.document import Document
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from united_knitting_mills.ukm.utils.python.employee_advance import advance_validation
class EmployeeAdvanceTool(Document):
	pass
@frappe.whitelist()
def employee_finder(location,designation=None,department=None):
	advance_percentage = frappe.db.get_single_value("United Knitting Mills Settings","advance_percentage")
	employee_names=[]
	filters= frappe._dict()
	filters.update({
		"location":location
	})
	if department:
		filters.update({"department":department})
	if designation:
		filters.update({"designation":designation})
	emp_list=frappe.db.get_all("Employee",filters=filters,fields=["name", "employee_name","designation"],order_by = "name")
	for name in emp_list:
		name.update({
			"eligible_amount":advance_validation(name['name']),
			"current_advance":((advance_validation(name['name']) or 0 )*advance_percentage)/100
		})
		employee_names.append(name)
	return employee_names
@frappe.whitelist()
def create_employee_advance(name,amount,eligible_amount,date,payment_type):
		make_property_setter(
				'Employee Advance', "purpose", "reqd", 0, "Data", validate_fields_for_doctype=False
		)
		make_property_setter(
				'Employee Advance', "advance_account", "reqd", 0, "Link", validate_fields_for_doctype=False
		)
		advance_doc=frappe.new_doc('Employee Advance')
		advance_doc.employee = name
		advance_doc.advance_amount = json.loads(amount)
		advance_doc.posting_date = date
		advance_doc.exchange_rate = 1.0
		advance_doc.eligible_amount = json.loads(eligible_amount) or 0
		if payment_type=="Deduct from Salary":
			advance_doc.repay_unclaimed_amount_from_salary=1
		advance_doc.insert()
		# advance_doc.submit()
		# frappe.db.commit()
