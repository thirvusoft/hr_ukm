# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
 
def execute(filters=None):
	attendance_date = filters.get("attendance_date")
	designation = filters.get("designation")
	department = filters.get("department")
	employee_conditions = ""
	if attendance_date or designation or department:
		employee_conditions = " where status = 'Active' "
		if department:
			employee_conditions += " and department = '{0}' ".format(department)
		if designation:
			employee_conditions += " and designation = '{0}' ".format(designation)
		
	
	employees = frappe.db.sql("""select name,employee_name, department, designation from `tabEmployee` {0} """.format(employee_conditions))
	data = [list(i) for i in employees]
	result_data = []
	settings = frappe.get_single("United Knitting Mills Settings")
	print(settings.checkin_type_resetting_time)
	date_time= attendance_date+" "+settings.checkin_type_resetting_time
	print(date_time)
	for i in range (0,len(data),1):
		# first_row = 1
		for logs in frappe.get_list("Employee Checkin Without Log Type",fields=["time"],filters={"employee": data[i][0],'time':['between',(attendance_date,attendance_date)], 'time':['>',date_time]},pluck='time'):
			# if first_row:
			result_data.append([data[i][0],data[i][1],data[i][2],data[i][3],logs.time()])
				# first_row = 0
			# else:
				# result_data.append(['','','','',logs.time()])
		# if first_row:
		# 	result_data.append([data[i][0],data[i][1],data[i][2],data[i][3],''])

	columns = get_columns()
	return columns, result_data

def get_columns():
    columns = [
		_("Employee Code") + ":Link/Employee:250",
		_("Employee Name") + ":Data:200",
		_("Department") + ":Link/Department:250",
        _("Designation") + ":Link/Designation:250",
        _("Logs") + ":Data:250",
        ]
    
    return columns
