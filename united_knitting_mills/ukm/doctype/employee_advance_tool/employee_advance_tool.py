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
		if doc.department not in ["PRODUCTION - MONTHLY - STAFF - UKM", "PRODUCTION - MONTHLY - STAFF - UNIT 1 - UKM"]:
			frappe.enqueue(create_employee_advance, doc = doc)
			frappe.msgprint("Advance Will Be Creating In Backgroud Within 10 Minutes.")
		else:
			frappe.enqueue(advance_staff, doc = doc)
			frappe.msgprint("Staff Advance Will Be Creating In Backgroud Within 10 Minutes.")

	def validate(doc):
		total_advance_amount = 0

		for row in doc.employee_advance_details:
			total_advance_amount += row.current_advance
			
		doc.total_advance_amount = total_advance_amount

	def on_cancel(doc):
		advance_cancel=frappe.get_all("Employee Advance", filters={"docstatus":["=", 1], "reference_document":doc.name} , pluck='name' )
		for i in advance_cancel:
			ea_doc=frappe.get_doc("Employee Advance", i)
			ea_doc.cancel()

	def on_trash(doc):
		employee_advance=frappe.get_all("Employee Advance", filters={"docstatus":["!=", 1], "reference_document":doc.name}, pluck='name' )
		for i in employee_advance:
			frappe.delete_doc("Employee Advance", i)
			

			

@frappe.whitelist()
def employee_finder(location, from_date, to_date, designation=None, department=None):

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
		fields = ["name", "employee_name", "designation", "department"],
		order_by = "name")
	
	for name in emp_list:
		total_eligible_amount_shift = list(advance_validation(name['name'], from_date, to_date))
		
		if not total_eligible_amount_shift[0]:
			total_eligible_amount_shift[0] = 0

		actual_advance = 0
		for allocated_advance in settings.advance_amount:
			
			if allocated_advance.maximum_salary <= total_eligible_amount_shift[0]:
				actual_advance = allocated_advance.advance_amount

		total_advance += actual_advance
		
		name.update({
			"eligible_amount": total_eligible_amount_shift[0],
			"current_advance": actual_advance,
			"total_shift": total_eligible_amount_shift[1]
		})
		employee_names.append(name)

	if not employee_names:
		frappe.throw("No Employees Found.", title=_("Message"))
		
	return employee_names, total_advance

@frappe.whitelist()
def create_employee_advance(doc):

		for advance in doc.employee_advance_details:
			
			if advance.eligible_amount:

				make_property_setter(
						'Employee Advance', "advance_account", "reqd", 0, "Link", validate_fields_for_doctype=False
				)

				advance_doc = frappe.new_doc('Employee Advance')

				advance_doc.employee = advance.employee
				advance_doc.from_date = doc.from_date
				advance_doc.to_date = doc.to_date
				advance_doc.advance_amount = advance.current_advance
				advance_doc.posting_date = nowdate()
				advance_doc.purpose = "Weekly Advance"
				advance_doc.exchange_rate = 1.0
				advance_doc.eligible_amount = advance.eligible_amount
				advance_doc.total_shift = advance.total_shift
				advance_doc.reference_document = doc.name

				if advance.payment_method == "Deduct from Salary":
					advance_doc.repay_unclaimed_amount_from_salary = 1

				advance_doc.insert()
				if not advance.hold:
					advance_doc.submit()
				else:
					advance_doc.is_hold=1
					advance_doc.save()
@frappe.whitelist()
def advance_staff(doc):
	for advance in doc.employee_advance_details:
		if advance.department in ["PRODUCTION - MONTHLY - STAFF - UKM", "PRODUCTION - MONTHLY - STAFF - UNIT 1 - UKM"]:
			make_property_setter(
						'Employee Advance', "advance_account", "reqd", 0, "Link", validate_fields_for_doctype=False
				)
			advance_doc = frappe.new_doc('Employee Advance')
			advance_doc.employee = advance.employee
			advance_doc.from_date = doc.from_date
			advance_doc.to_date = doc.to_date
			advance_doc.advance_amount = advance.staff_advance
			advance_doc.monthly_deduction = advance.monthly_deduction
			advance_doc.balance_amount = advance.staff_advance
			advance_doc.posting_date = nowdate()
			advance_doc.purpose = "Staff Advance"
			advance_doc.exchange_rate = 1.0
			advance_doc.eligible_amount = advance.eligible_amount
			advance_doc.total_shift = advance.total_shift
			advance_doc.reference_document = doc.name

			if advance.payment_method == "Deduct from Salary":
					advance_doc.repay_unclaimed_amount_from_salary = 1
			advance_doc.insert()
			if not advance.hold:
				advance_doc.submit()
			else:
				advance_doc.is_hold=1
				advance_doc.save()

