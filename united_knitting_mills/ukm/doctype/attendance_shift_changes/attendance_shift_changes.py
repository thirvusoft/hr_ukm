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
			if not attendance.staff and ssa:
				attendance.update({"total_shift_count":final_shift_count, "total_shift_amount":ssa[0]['base']*final_shift_count})
			else:
				attendance.update({"total_shift_count":final_shift_count})
			attendance.save()
	def onload(self):
		shift_detail=frappe.db.get_all("Attendance Shift Changes", filters={"docstatus":["!=", 2], "attendance":self.attendance, "workflow_state": ["!=","Rejected"]})
		if len(shift_detail)>1:
			frappe.throw("This Attendance, Shift Changes Already Created")
			