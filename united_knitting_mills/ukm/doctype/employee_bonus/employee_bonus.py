# Copyright (c) 2022, Ts Hr and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeBonus(Document):
	def on_submit(self):
			payment_doc=frappe.new_doc('Payment Entry')
			payment_doc.payment_type = 'Pay'
			payment_doc.party_type = 'Employee'
			payment_doc.party = self.employee
			company = frappe.get_doc('Company',self.company)
			abbr=company.abbr
			payment_doc.posting_date=self.bonus_payment_date
			payment_doc.paid_amount=self.bonus_amount
			payment_doc.received_amount=self.bonus_amount
			payment_doc.source_exchange_rate=1.0
			payment_doc.paid_from=self.bonus_account
			payment_doc.paid_from_account_currency=company.default_currency
			payment_doc.paid_to = 'Creditors - '+abbr
			payment_doc.employee_bonus_reference = self.name
			payment_doc.submit()
	def on_cancel(self):
		pe=frappe.db.get_all("Payment Entry", filters={'docstatus':1, "employee_bonus_reference":self.name}, pluck='name' )
		for i in pe:
			pe_doc=frappe.get_doc("Payment Entry", i)
			pe_doc.cancel()
		self.ignore_linked_doctypes = ("GL Entry")

	def on_trash(self):
		pe=frappe.get_all("Payment Entry", filters={'docstatus':2, "employee_bonus_reference":self.name} , pluck='name' )
		for i in pe:
			frappe.delete_doc("Payment Entry", i)
