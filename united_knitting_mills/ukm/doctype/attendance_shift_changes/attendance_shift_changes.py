# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AttendanceShiftChanges(Document):
	def on_update(self):
		if self.workflow_state == "Approved":
			attendance=frappe.get_doc("Attendance", self.attendance)
			ssa=frappe.db.get_all("Salary Structure Assignment", filters={"employee":self.employee, "docstatus":1}, fields=["base"])
			final_shift_count = self.total_shift_count + self.update_shift_count
			if not attendance.staff:
				attendance.update({"total_shift_count":final_shift_count, "total_shift_amount":ssa[0]['base']*final_shift_count})
			else:
				attendance.update({"total_shift_count":final_shift_count})
			attendance.save()
