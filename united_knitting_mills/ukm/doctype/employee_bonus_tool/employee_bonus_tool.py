import frappe
import json
from frappe.model.document import Document

class EmployeeBonusTool(Document):
	pass
@frappe.whitelist()
def employee_finder(bonus1):
	employee_names=[]
	a=frappe.db.get_all("Employee",filters={"designation":bonus1},fields=["name", "employee_name"])
	for name in a:
		employee_names.append(name)
	return employee_names

@frappe.whitelist()
def create_bonus(name,amount,date,doc):
	amount=json.loads(amount)
	bonus_doc=frappe.new_doc('Employee Bonus')
	bonus_doc.employee = name
	bonus_doc.bonus_payment_date= date
	bonus_doc.bonus_amount = amount
	bonus_doc.reference=doc
	bonus_doc.insert()
	bonus_doc.save()
	bonus_doc.submit()
	frappe.db.commit()
