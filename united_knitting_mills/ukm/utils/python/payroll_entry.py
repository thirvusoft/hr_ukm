import frappe
from frappe.utils import nowdate,add_days
from erpnext.payroll.doctype.payroll_entry.payroll_entry import ( PayrollEntry,get_existing_salary_slips)
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
import frappe
from frappe.utils import getdate
from frappe import _

def validate_to_date(doc,event):

	if (doc.end_date >= nowdate()):
		doc.end_date = add_days(nowdate(),-1)
		frappe.msgprint(f'End Date cannot be greater than Yesterday ({doc.end_date}). Valid date is applied.')


# Override Function -> Start & End Date Should Not Be Changed
@frappe.whitelist()
def get_start_end_dates(payroll_frequency, start_date=None, company=None):
	pass

class FoodExpense(PayrollEntry):
	@frappe.whitelist()
	def create_salary_slips(self):
		self.check_permission("write")
		employees = [emp.employee for emp in self.employees]
		food_count= [emp.food_expense for emp in self.employees]
		medical_exp=[emp.medical_expense for emp in self.employees]
		maintenance_exp=[emp.maintenance_expense for emp in self.employees]
		rent_exp=[emp.rent_expense for emp in self.employees]
		late_ded=[emp.late_deduction for emp in self.employees]
		is_hold=[emp.is_hold for emp in self.employees]
		esi=[emp.esi for emp in self.employees]
		pf=[emp.pf for emp in self.employees]
		if employees:
			args = frappe._dict(
				{
					"salary_slip_based_on_timesheet": self.salary_slip_based_on_timesheet,
					"payroll_frequency": self.payroll_frequency,
					"start_date": self.start_date,
					"end_date": self.end_date,
					"company": self.company,
					"posting_date": self.posting_date,
					"deduct_tax_for_unclaimed_employee_benefits": self.deduct_tax_for_unclaimed_employee_benefits,
					"deduct_tax_for_unsubmitted_tax_exemption_proof": self.deduct_tax_for_unsubmitted_tax_exemption_proof,
					"payroll_entry": self.name,
					"exchange_rate": self.exchange_rate,
					"currency": self.currency,
				}
			)
			if len(employees) > 30:
				frappe.enqueue(create_salary_slips_for_employees, timeout=600, employees=employees,args=args,food_count=food_count, medical_exp=medical_exp, maintenance_exp=maintenance_exp, rent_exp=rent_exp, late_ded=late_ded,is_hold=is_hold,esi=esi,pf=pf)
			else:
				create_salary_slips_for_employees(employees, args,food_count, medical_exp, maintenance_exp,rent_exp,late_ded,is_hold,esi,pf, publish_progress=False)
				# since this method is called via frm.call this doc needs to be updated manually
				self.reload()
	@frappe.whitelist()
	def submit_salary_slips(self):
		self.check_permission("write")
		ss_list = self.get_sal_slip_list(ss_status=0)
		if len(ss_list) > 30:
			frappe.enqueue(
				submit_salary_slips_for_employees, timeout=600, payroll_entry=self, salary_slips=ss_list
			)
		else:
			submit_salary_slips_for_employees(self, ss_list, publish_progress=False)

def create_salary_slips_for_employees(employees, args,food_count,medical_exp, maintenance_exp, rent_exp,late_ded,is_hold,esi,pf, publish_progress=True):
	salary_slips_exists_for = get_existing_salary_slips(employees, args)
	count = 0
	salary_slips_not_created = []
	index = 0
	for emp in employees:
		if emp not in salary_slips_exists_for:
			args.update({"doctype": "Salary Slip", "food_expense_days": food_count[index], "medical_expense":medical_exp[index], "maintenance_expense":maintenance_exp[index], "rent_expense":rent_exp[index], "late_deduction": late_ded[index], "is_hold":is_hold[index], "esi":esi[index], "pf":pf[index]}) 
			args.update({"doctype": "Salary Slip", "employee": emp})
			ss = frappe.get_doc(args)
			ss.insert()
			count += 1
			if publish_progress:
				frappe.publish_progress(
					count * 100 / len(set(employees) - set(salary_slips_exists_for)),
					title=_("Creating Salary Slips..."),
				)
		
		else:
			salary_slips_not_created.append(emp)
		index+=1

	payroll_entry = frappe.get_doc("Payroll Entry", args.payroll_entry)
	payroll_entry.db_set("salary_slips_created", 1)
	payroll_entry.notify_update()

	if salary_slips_not_created:
		frappe.msgprint(
			_(
				"Salary Slips already exists for employees {}, and will not be processed by this payroll."
			).format(frappe.bold(", ".join([emp for emp in salary_slips_not_created]))),
			title=_("Message"),
			indicator="orange",
		)

def submit_salary_slips_for_employees(payroll_entry, salary_slips, publish_progress=True):
	submitted_ss = []
	not_submitted_ss = []
	frappe.flags.via_payroll_entry = True

	count = 0
	for ss in salary_slips:
		ss_obj = frappe.get_doc("Salary Slip", ss[0])
		if ss_obj.net_pay <= 0:
			not_submitted_ss.append(ss[0])
		else:
			try:
				if not ss_obj.is_hold:
					ss_obj.submit()
					submitted_ss.append(ss_obj)
			except frappe.ValidationError:
				not_submitted_ss.append(ss[0])

		count += 1
		if publish_progress:
			frappe.publish_progress(count * 100 / len(salary_slips), title=_("Submitting Salary Slips..."))
	if submitted_ss:
		payroll_entry.make_accrual_jv_entry()
		frappe.msgprint(
			_("Salary Slip submitted for period from {0} to {1}").format(ss_obj.start_date, ss_obj.end_date)
		)

		payroll_entry.email_salary_slip(submitted_ss)

		payroll_entry.db_set("salary_slips_submitted", 1)
		payroll_entry.notify_update()

	if not submitted_ss and not not_submitted_ss:
		frappe.msgprint(
			_(
				"No salary slip found to submit for the above selected criteria OR salary slip already submitted"
			)
		)

	if not_submitted_ss:
		frappe.msgprint(_("Could not submit some Salary Slips"))

	frappe.flags.via_payroll_entry = False


# def html_history(single_slip,payroll_entry):
# 	html='<tr style="border: 1px solid #ddd; height:20px !important;">'+''.join([ 
# 		f'<th style="border-right: 1px solid #ddd;"><center>{i}</center></th>'for i in ['S.No','Employee','Salary Issued'] ])+'</tr>'
# 	td=[
# 		f'<tr style="text-align:center;border: 1px solid #ddd; height:20px !important;"><h1>'+
# 		f'<td style="border-right: 1px solid #ddd;">{i+1}</td>'+
# 		f'<td style="border-right: 1px solid #ddd;">{single_slip[i]["Employee"]}</td>'+
# 		f'<td style="border-right: 1px solid #ddd;">{single_slip[i]["Salary"]}</td>'+'</tr></h1>'
# 		for i in range(len(single_slip))
# 		]
# 	value ='<table style="width:100%;border: 1px solid #ddd;border-collapse: collapse; ">'+html+''.join(td)+'</table>'
# 	frappe.set_value(payroll_entry.doctype, payroll_entry.name, "employee_salary_",value)