from . import __version__ as app_version
import frappe
app_name = "united_knitting_mills"
app_title = "UKM"
app_publisher = "UKM"
app_description = "UKM"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "UKM"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/united_knitting_mills/css/united_knitting_mills.css"
# app_include_js = "/assets/united_knitting_mills/js/united_knitting_mills.js"

# include js, css files in header of web template
# web_include_css = "/assets/united_knitting_mills/css/united_knitting_mills.css"
# web_include_js = "/assets/united_knitting_mills/js/united_knitting_mills.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "united_knitting_mills/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
doctype_js = {"Employee" : "ukm/utils/javascript/employee.js",
		#  "Salary Structure Assignment" : "ukm/utils/javascript/salary_structure_assignment.js",
		 "Journal Entry":"ukm/utils/javascript/journal_entry.js",
		 "Location":"ukm/utils/javascript/location.js",
		 "Holiday List":"ukm/utils/javascript/holiday_list.js",
		 "Leave Application":"ukm/utils/javascript/leave_application.js",
		 "Payroll Entry" : "ukm/utils/javascript/payroll_entry.js",
   		 "Employee Advance":"ukm/utils/javascript/employee_advance.js"
		}
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"Department" : "ukm/utils/javascript/department_list.js",
			"Designation":"ukm/utils/javascript/designation_list.js",
			"Holiday List":"ukm/utils/javascript/holiday_list_list.js",
			"Employee":"ukm/utils/javascript/employee_list.js",
			"Leave Application":"ukm/utils/javascript/leave_application_list.js",
			"Attendance":"ukm/utils/javascript/attendance_list.js",
			"Salary Slip":"ukm/utils/javascript/salary_slip_list.js",
			"Payroll Entry":"ukm/utils/javascript/payroll_entry_list.js",
			"Salary Structure":"ukm/utils/javascript/salary_structure_list.js",
			"Salary Structure Assignment":"ukm/utils/javascript/salary_structure_assignment_list.js",
			"Attendance":"ukm/utils/javascript/attendance.js",
   			"Employee Advance":"ukm/utils/javascript/employee_advance_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "united_knitting_mills.install.before_install"
after_install = "united_knitting_mills.after_install.create_custom_fields"
# after_migrate = "united_knitting_mills.ukm.custom_fields.hr.employee.employee_fields"

# Uninstallation
# ------------

# before_uninstall = "united_knitting_mills.uninstall.before_uninstall"
# after_uninstall = "united_knitting_mills.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "united_knitting_mills.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Leave Application": "united_knitting_mills.ukm.utils.python.leave_application.TsLeaveApplication",
	"Payroll Entry":"united_knitting_mills.ukm.utils.python.payroll_entry.FoodExpense"
}


# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
	"Salary Slip":{
		"validate":"united_knitting_mills.ukm.utils.python.salary_slip.set_salary_for_labour",
		"validate":"united_knitting_mills.ukm.utils.python.salary_slip.food_expens_amount"
	},

	'Employee':{
		"validate":"united_knitting_mills.ukm.utils.python.employee.address_html",
		"after_insert":["united_knitting_mills.ukm.utils.python.employee.creating_hr_permission",
		"united_knitting_mills.ukm.utils.python.employee.bio_metric_id"]
	},

	'Attendance':{
		"validate":"united_knitting_mills.ukm.utils.python.attendance.validate_shift_details",
		"on_update":"united_knitting_mills.ukm.utils.python.attendance.update_time_field",
		"on_submit":"united_knitting_mills.ukm.utils.python.attendance.requested_amount_to_total",
		"on_trash": "united_knitting_mills.ukm.utils.python.attendance.unlink_logs",
	},

	'Additional Salary':{
		"on_submit":"united_knitting_mills.ukm.utils.python.additional_salary.on_submit",
		# "on_cancel":"united_knitting_mills.ukm.utils.python.additional_salary.payment_cancel",

	},

	'Payroll Entry':{
		"validate":"united_knitting_mills.ukm.utils.python.payroll_entry.validate_to_date",
	},

 	"Employee Bonus Tool":{
		"validate":"united_knitting_mills.ukm.doctype.employee_bonus_tool.employee_bonus_tool.total_bonus_amt_total",
		"on_submit":"united_knitting_mills.ukm.doctype.employee_bonus_tool.employee_bonus_tool.create_bonus"
	},

	"Leave Application":{
		"validate":"united_knitting_mills.ukm.utils.python.leave_application.validating_leave",
		"on_submit":"united_knitting_mills.ukm.utils.python.leave_application.attendance_updation"
	},

	"Salary Structure Assignment":{
		"on_submit":"united_knitting_mills.ukm.utils.python.salary_structure_assignment.salary_updation",
		"validate":"united_knitting_mills.ukm.utils.python.salary_structure_assignment.validation"
	},
	"Employee Advance":{
		"on_cancel":["united_knitting_mills.ukm.utils.python.employee_advance.employee_advance_cancel",
					"united_knitting_mills.ukm.utils.python.employee_advance.additional_salary_cancel"],
		"on_trash":["united_knitting_mills.ukm.utils.python.employee_advance.employee_advance_delete",
					"united_knitting_mills.ukm.utils.python.employee_advance.additional_salary_delete"]

	}

	# "Location":{
	# 	"validate":["united_knitting_mills.ukm.utils.python.location.sequence_user_id",
	# 				"united_knitting_mills.ukm.utils.python.location.autoname"]
	# }
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
	"daily": [
		"united_knitting_mills.tasks.all"
	],
 	"cron":{
	
	}
	# "daily": [
	# 	"united_knitting_mills.tasks.daily"
	# ],
	# "hourly": [
	# 	"united_knitting_mills.tasks.hourly"
	# ],
	# "weekly": [
	# 	"united_knitting_mills.tasks.weekly"
	# ]
	# "monthly": [
	# 	"united_knitting_mills.tasks.monthly"
	# ]
}
try:
	time = str(frappe.db.get_single_value('United Knitting Mills Settings', 'checkin_type_resetting_time'))
	time = time.split(':')
	cron_time = f'{int(time[1])} {int(time[0])} * * *'
	scheduler_events['cron'][cron_time] = ['united_knitting_mills.ukm.utils.python.employee__checkin.create_employee_checkin']
except:pass

# Testing
# -------

# before_tests = "united_knitting_mills.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "united_knitting_mills.event.get_events"
# }
override_whitelisted_methods = {
	"erpnext.payroll.doctype.payroll_entry.payroll_entry.get_start_end_dates": "united_knitting_mills.ukm.utils.python.payroll_entry.get_start_end_dates"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "united_knitting_mills.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"united_knitting_mills.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
