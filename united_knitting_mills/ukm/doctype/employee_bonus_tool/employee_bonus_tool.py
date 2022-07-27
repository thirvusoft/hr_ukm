import frappe
import json
from frappe.model.document import Document

class EmployeeBonusTool(Document):
	pass
@frappe.whitelist()
def employee_finder(bonus1,location,from_date,to_date):
	employee_names=[]
	amount=[]
	
	emp_list=frappe.db.get_all("Employee",filters={"designation":bonus1,'location':location},fields=["name", "employee_name"])
	bonus_percent= frappe.db.get_single_value("United Knitting Mills Settings" , "bonus_percentage")
	for name in emp_list:
		
		attendance_status = frappe.db.sql("""
			SELECT count(att.name)
			FROM `tabAttendance` as att
			WHERE  att.employee = '{0}' and att.attendance_date between '{1}' and '{2}' and att.status = 'Present'
			""".format(name['name'],from_date,to_date),as_list=1)[0][0]


		emp_base_amount=frappe.db.sql("""select ssa.base
				FROM `tabSalary Structure Assignment` as ssa
				WHERE ssa.employee = '{0}' and ssa.from_date <='{1}'
				ORDER BY ssa.from_date DESC LIMIT 1 """.format(name['name'],to_date),as_list=1)
	
		if emp_base_amount:
			calc = (float(attendance_status) * float(emp_base_amount[0][0])) * ( bonus_percent/ 100)

			amount.append(calc)
		employee_names.append(name)
		
	return employee_names,amount

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



	



