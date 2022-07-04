import frappe

from frappe.model.document import Document
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

class EmployeeAdvanceTool(Document):
	pass
@frappe.whitelist()
def employee_finder(advance1,location):
	employee_names=[]
	emp_list=frappe.db.get_all("Employee",filters={"designation":advance1,'location':location},fields=["name", "employee_name"])
	for name in emp_list:
		employee_names.append(name)
	return employee_names
@frappe.whitelist()
def create_employee_advance(name,amount,date,payment_type):
		make_property_setter(
				'Employee Advance', "purpose", "reqd", 0, "Data", validate_fields_for_doctype=False
		)
		make_property_setter(
				'Employee Advance', "advance_account", "reqd", 0, "Link", validate_fields_for_doctype=False
		)
		advance_doc=frappe.new_doc('Employee Advance')
		advance_doc.employee = name
		advance_doc.advance_amount = amount
		advance_doc.posting_date = date
		advance_doc.exchange_rate = 1.0
		if payment_type=="Deduct from Salary":
			advance_doc.repay_unclaimed_amount_from_salary=1
		advance_doc.insert()
		advance_doc.save()
		advance_doc.submit()
		frappe.db.commit()
