# Copyright (c) 2022, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class EmployeeCheckinWithoutLogType(Document):

	def validate(self):
		
		doc = frappe.db.exists(
			"Employee Checkin Without Log Type", {"employee": self.employee, "time": self.time, "name": ["!=", self.name]}
		)
		if doc:
			doc_link = frappe.get_desk_link("Employee Checkin Without Log Type", doc)
			frappe.throw(
				_("This employee already has a log with the same timestamp.{0}").format("<Br>" + doc_link)
			)
