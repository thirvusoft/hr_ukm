# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
 
def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	designation = filters.get("designation")
	department = filters.get("department")
	conditions = ""
	if from_date or to_date or department or designation:
		conditions = " where 1 = 1"
		# if from_date and to_date:
		# 	conditions += "  and start_date = '{0}' and end_date = '{0}' ".format(from_date,to_date)
		if designation:
			conditions += " and designation = '{0}' ".format(designation)
		if department:
			conditions += " and designation = '{0}' ".format(department)
		
	employees = frappe.db.sql("""select name,employee_name,designation,department from `tabEmployee` {0} """.format(conditions))
	data = [list(i) for i in employees]
	result_data = []
	for i in range (0,len(data),1):
		first_row = 1
		for logs in frappe.get_list("Salary Slip",fields=["start",''],filters={"employee": data[i][0],'time':['between',(attendance_date,attendance_date)]},pluck='time'):
			if first_row:
				result_data.append([f'<b>{data[i][0]}</b>',data[i][1],data[i][2],data[i][3],logs.time()])
				first_row = 0
			else:
				result_data.append(['','','','',logs.time()])
		if first_row:
			result_data.append([f'<b>{data[i][0]}</b>',data[i][1],data[i][2],data[i][3],''])

    report_data = frappe.db.sql(""" select
    							att.designation,
                                att.name,
                                att.employee,
                                att.employee_name,
                                att.checkin_time,
                                att.checkout_time,
                                att.late_min,
                                att.total_shift_count,
                                doc.check_in_time,
                                doc.check_out_time
                                from `tabAttendance` as att left outer join `tabThirvu Employee Checkin Details` as doc
                                on doc.parent = att.name
                                {0} order by designation
                                """.format(conditions))
	# check =''
	# for i in range (0,len(data),1):
	# 	if data[i][0] != check:
	# 		check = data[i][0] 
	# 		data[i][0] = f'<b>{data[i][0]}</b>'

	# 	else:
	# 		data[i][0]=''
	# 	if data[i][8]:
	# 		data[i][4] = data[i][8]
	# 	if data[i][9]:
	# 		data[i][5] = data[i][9]
	columns = get_columns()
	return columns, data
 
def get_columns():
	columns = [
		_("Employee Code") + ":Link/Employee:250",
		_("Employee Name") + ":Data:200",
		_("Designation") + ":Link/Designation:250",
		_("Department") + ":Link/Department:250",
		]
	
	return columns
