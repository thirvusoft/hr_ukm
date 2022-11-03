from frappe.utils.data import getdate
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
import frappe
from frappe import _

import datetime
from dateutil.relativedelta import relativedelta

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


@frappe.whitelist()
def leave_type_filter(department = None):

    filtered_leave_type = []
    
    if department:
        is_staff_department = frappe.get_value("Department",department,"is_staff")

        if not is_staff_department:
            leave_type_name = frappe.get_all("Leave Type",{"is_pay_leave":0})

            for name in leave_type_name:
                filtered_leave_type.append(name["name"])

    if not filtered_leave_type:
        leave_type_name = frappe.get_all("Leave Type")

        for name in leave_type_name:
            filtered_leave_type.append(name["name"])

    return filtered_leave_type

@frappe.whitelist()
def validating_pay_leave(doc, event):

    if frappe.get_value("Leave Type",doc.leave_type,"is_pay_leave"):

        if doc.from_date == doc.to_date:

            if doc.half_day:
                frappe.throw("For Pay Leave, Half Day Is Not Allowed.")

            else:
                
                last_date_of_month = getdate(doc.from_date) + relativedelta(day=1, months=+1, days=-1)
                first_date_of_month = getdate(doc.from_date) + relativedelta(day=1)

                leave_type = frappe.get_value("Leave Type",doc.leave_type,"name")

                leave_application = frappe.get_all("Leave Application",{
                    "employee":doc.employee,
                    "leave_type":leave_type,
                    "status":"Approved",
                    "from_date":["between", (first_date_of_month, last_date_of_month)]
                    },
                "name")

                if leave_application:
                    allocated_leave = frappe.db.get_single_value("United Knitting Mills Settings","pay_leave")

                    if allocated_leave < len(leave_application):
                        frappe.throw("Already You Consumed Pay Leave For This Month.",title=_("Message"))
                else:
                    doc.is_pay_leave_application = 1
        else:
            frappe.throw("For Pay Leave, From Date And To Date Should Be Same Date.",title=_("Message"))
            