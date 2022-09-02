from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
import frappe
from frappe import _

from erpnext.hr.utils import (
	get_holiday_dates_for_employee,
	get_leave_period,
	set_employee_name,
	share_doc_with_approver,
	validate_active_employee,
)


class TsLeaveApplication(LeaveApplication):
    def validate(self):
        if(self.leave_type not in ['Permission', 'On Duty']):
            validate_active_employee(self.employee)
            set_employee_name(self)
            self.validate_dates()
            self.validate_balance_leaves()
            self.validate_leave_overlap()
            self.validate_max_days()
            self.show_block_day_warning()
            self.validate_block_days()
            self.validate_salary_processed_days()
            self.validate_attendance()
            self.set_half_day_date()
            if frappe.db.get_value("Leave Type", self.leave_type, "is_optional_leave"):
                self.validate_optional_leave()
            self.validate_applicable_after()

    def on_submit(self):
        if self.status in ["Open", "Cancelled"]:
            frappe.throw(
                _("Only Leave Applications with status 'Approved' and 'Rejected' can be submitted")
            )

        self.validate_back_dated_application()
        if self.leave_type not in ['On Duty','Permission']:
            self.update_attendance()

        # notify leave applier about approval
        if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
            self.notify_employee()

        self.create_leave_ledger_entry()
        self.reload()