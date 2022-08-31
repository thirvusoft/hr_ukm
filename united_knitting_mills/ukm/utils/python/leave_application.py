from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
import frappe
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