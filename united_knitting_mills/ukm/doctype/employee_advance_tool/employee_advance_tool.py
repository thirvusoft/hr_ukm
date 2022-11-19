import json

import frappe
from frappe import _
from frappe.custom.doctype.property_setter.property_setter import \
    make_property_setter
from frappe.model.document import Document
from frappe.utils import (add_days,nowdate,)
from united_knitting_mills.ukm.utils.python.employee_advance import \
    advance_validation


class EmployeeAdvanceTool(Document):

	def on_submit(doc):
		frappe.enqueue(create_employee_advance, doc = doc)
		frappe.msgprint("Advance Will Be Creating In Backgroud Within 5 Mins")

@frappe.whitelist()
def employee_finder(location,from_date,to_date,designation=None,department=None):

	settings = frappe.get_doc("United Knitting Mills Settings", "United Knitting Mills Settings")
	
	if not settings.advance_amount:
		frappe.throw("Not Allocated The Advance Details, Please Contact Your Administrator.", title=_("Message"))
	
	employee_names = []
	total_advance = 0

	filters = frappe._dict()

	filters.update({"status": "Active"})
	filters.update({"location": location})

	if department:
		filters.update({"department": department})

	if designation:
		filters.update({"designation": designation})

	emp_list = frappe.db.get_all("Employee",
		filters = filters,
		fields = ["name", "employee_name", "designation"],
		order_by = "name")
	
	for name in emp_list:
		total_eligible_amount = advance_validation(name['name'], from_date, to_date)
		
		if not total_eligible_amount:
			total_eligible_amount = 0

		actual_advance = 0
		for allocated_advance in settings.advance_amount:
			
			if allocated_advance.maximum_salary <= total_eligible_amount:
				actual_advance = allocated_advance.advance_amount

		total_advance += actual_advance
		
		name.update({
			"eligible_amount": total_eligible_amount,
			"current_advance":actual_advance
		})
		employee_names.append(name)

	if not employee_names:
		frappe.throw("No Employees Found.", title=_("Message"))
		
	return employee_names, total_advance

@frappe.whitelist()
def create_employee_advance(doc):

		for advance in doc.employee_advance_details:
			
			if advance.current_advance:

				make_property_setter(
						'Employee Advance', "advance_account", "reqd", 0, "Link", validate_fields_for_doctype=False
				)

				advance_doc = frappe.new_doc('Employee Advance')

				advance_doc.employee = advance.employee
				advance_doc.advance_amount = advance.current_advance
				advance_doc.posting_date = nowdate()
				advance_doc.purpose = "Weekly Advance"
				advance_doc.exchange_rate = 1.0
				advance_doc.eligible_amount = advance.eligible_amount
				advance_doc.reference_document = doc.name

				if advance.payment_method == "Deduct from Salary":
					advance_doc.repay_unclaimed_amount_from_salary = 1

				advance_doc.insert()
				advance_doc.submit()
