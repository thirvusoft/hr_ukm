# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeBankDetails(Document):
	def on_update(self):
		if self.workflow_state == "Approved":
			employee=frappe.get_doc("Employee", self.employee)
			employee.update({"bank_name":self.bank_name,"ts_bank_branch_name":self.branch_name, "bank_ac_no":self.bank_ac_no,
			                   "ifsc_code":self.ifsc_code, "micr_code":self.micr_code})
			employee.save(ignore_permissions = True)
