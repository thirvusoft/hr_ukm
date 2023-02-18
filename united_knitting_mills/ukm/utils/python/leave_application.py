from frappe.utils.data import getdate
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
import frappe
from frappe import _

import datetime
from dateutil.relativedelta import relativedelta

from frappe.utils.data import today, get_datetime

from erpnext.hr.utils import (
	get_holiday_dates_for_employee,
	get_leave_period,
	set_employee_name,
	share_doc_with_approver,
	validate_active_employee,
)


class TsLeaveApplication(LeaveApplication):
    def validate(self):
        if(self.leave_type not in ['Permission', 'On Duty', 'Pay Leave']):
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
        if self.leave_type not in ['On Duty','Permission','Pay Leave']:
            self.update_attendance()

        # notify leave applier about approval
        if frappe.db.get_single_value("HR Settings", "send_leave_notification"):
            self.notify_employee()

        self.create_leave_ledger_entry()
        self.reload()


@frappe.whitelist()
def employee_staff_filter():

    filtered_staff_employees = []
    
    is_staff_department = frappe.get_all("Department", {"is_staff": 1})

    for staff_department in is_staff_department:
        staff_employees = frappe.get_all("Employee", {"department":staff_department.name,"status": "Active"})
    
        for employee in staff_employees:
            filtered_staff_employees.append(employee.name)

    return filtered_staff_employees

@frappe.whitelist()
def validating_leave(doc, event):

    if frappe.get_value("Leave Type",doc.leave_type,"is_pay_leave"):

        if doc.from_date == doc.to_date:

            if doc.half_day:
                total_leave_application_count = 0.50

            else:
                total_leave_application_count = 1

            last_date_of_month = getdate(doc.from_date) + relativedelta(day=1, months=+1, days=-1)
            first_date_of_month = getdate(doc.from_date) + relativedelta(day=1)

            leave_applications = frappe.get_all("Leave Application",filters = {
                "employee":doc.employee,
                "leave_type":doc.leave_type,
                "status":"Approved",
                "docstatus":1,
                "from_date":["between", (first_date_of_month, last_date_of_month)]
                },
                fields = ["half_day"])

            
            allocated_leave = frappe.db.get_single_value("United Knitting Mills Settings","pay_leave")

            for leave_application in leave_applications:

                if leave_application["half_day"] == 1:
                    total_leave_application_count += 0.50

                else:
                    total_leave_application_count += 1
            
            if allocated_leave == 0:
                frappe.throw("Not Allowed For Pay Leave, Please Contact Your Administrator.",title=_("Message"))
            
            elif allocated_leave < total_leave_application_count:
                frappe.throw("Already You Consumed Pay Leave For This Month, Please Contact Your Administrator.",title=_("Message"))
            
            else:
                doc.is_pay_leave_application = 1
        else:
            frappe.throw("For Pay Leave, From Date And To Date Should Be Same Date.",title=_("Message"))

    elif doc.leave_type == "Permission":

        last_date_of_month = getdate(doc.attendance_date) + relativedelta(day=1, months=+1, days=-1)
        first_date_of_month = getdate(doc.attendance_date) + relativedelta(day=1)

        leave_application = frappe.get_all("Leave Application",{
                    "employee":doc.employee,
                    "leave_type":doc.leave_type,
                    "status":"Approved",
                    "docstatus":1,
                    "attendance_date":["between", (first_date_of_month, last_date_of_month)]
                    },
                "name")

        
        allocated_permission = frappe.db.get_single_value("United Knitting Mills Settings","permission_leave")
        allocated_time = frappe.db.get_single_value("United Knitting Mills Settings","time_in_minutes")
        
        actual_time = datetime.datetime.strptime(doc.to_time, "%H:%M:%S") - datetime.datetime.strptime(doc.from_time, "%H:%M:%S")
        
        if doc.from_time >= doc.to_time:
            frappe.throw("To Time Is Less than or Equal to From Time, Please check it.",title=_("Message"))
        
        elif allocated_permission == 0 or allocated_time == 0:
            frappe.throw("Not Allowed For Permission, Please Contact Your Administrator.",title=_("Message"))
        
        elif allocated_permission <= len(leave_application):
            frappe.throw("Already You Consumed Permission For This Month, Please Contact Your Administrator.",title=_("Message"))

        elif allocated_time < actual_time.total_seconds() / 60:
            frappe.throw(f"Permission Time Is Greater Than The Allocated Permission Time : {allocated_time}.",title=_("Message"))
            
    # To Change the Leave Application State as same as Workflow State
    if doc.workflow_state in ["Approved", "Rejected"]:
        doc.status = doc.workflow_state

@frappe.whitelist()
def attendance_updation(doc, event):
    if doc.workflow_state == "Approved":
        if doc.leave_type != 'Pay Leave':
            if frappe.db.exists('Attendance',{"attendance_date": doc.attendance_date,"employee": doc.employee, "docstatus":["!=", 2]}):

                existing_doc = frappe.get_doc('Attendance',{"attendance_date": doc.attendance_date,"employee":doc.employee, "docstatus":["!=", 2]})
                
                if existing_doc.docstatus:
                    new_doc = frappe.copy_doc(existing_doc)
                    new_doc.workflow_state = "Draft"
                    existing_doc.workflow_state = "Cancelled"
                    existing_doc.cancel()
                    
                    new_doc.amended_from = existing_doc.name
                    
                    new_doc.update({
                        'leave_application': doc.name,
                        'leave_type': doc.leave_type
                        })
                    new_doc.insert()

                    doc.attendance_marked = 1
                    doc.save()

                else:
                    existing_doc.update({
                        'leave_application': doc.name,
                        'leave_type': doc.leave_type
                        })
                    existing_doc.save()

                    doc.attendance_marked = 1
                    doc.save()
                    
                
            else:
                
                if get_datetime(doc.attendance_date) < get_datetime(today()):

                    attendance = frappe.new_doc('Attendance')
                    attendance.employee = doc.employee
                    attendance.attendance_date = doc.attendance_date
                    attendance.leave_application = doc.name
                    attendance.leave_type = doc.leave_type
                    attendance.staff=1
                    attendance.checkin_time = doc.from_time
                    attendance.checkout_time = doc.to_time
                    attendance.save()

                    doc.attendance_marked = 1
                    doc.save()
            
