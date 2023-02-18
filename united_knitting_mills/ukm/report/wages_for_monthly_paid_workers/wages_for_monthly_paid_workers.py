# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
 
def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	designation = filters.get("designation")
	department = filters.get("department")
	location = filters.get("location")
	conditions = ""
	if from_date or to_date or department or designation or location:
		conditions = " where status = 'Active'"
		# if from_date and to_date:
		# 	conditions += "  and start_date = '{0}' and end_date = '{1}' ".format(from_date,to_date)
		if designation:
			conditions += " and designation = '{0}' ".format(designation)
		if department:
			conditions += " and department = '{0}' ".format(department)
		if location:
			conditions += " and location = '{0}' ".format(location)
		
		
	employees = frappe.db.sql("""select name,employee_name,designation,department from `tabEmployee` {0} """.format(conditions))
	data = [list(i) for i in employees]
	result_data = []
	for i in range (0,len(data),1):
		first_row = 1
		for slip in frappe.get_list("Salary Slip",fields=["name","payment_days",'total_working_days','net_pay','total_deduction','extra_minutes','gross_pay','ts_shift_amount'],filters={"docstatus":1,"employee": data[i][0],'start_date':['>=',(from_date)],'end_date':['<=',(to_date)]}):
			result_data.append([data[i][0],data[i][1],data[i][2],data[i][3],slip['name'],slip['payment_days'],slip['total_working_days'],slip['extra_minutes'],slip['ts_shift_amount'],slip['gross_pay'],0,slip['gross_pay'],0,0,slip['total_deduction'],slip['net_pay']])			
			
	columns = get_columns()
	return columns, result_data
 
def get_columns():
	columns = [
		_("Employee Code") + ":Link/Employee:200",
		_("Employee Name") + ":Data:100",
		_("Designation") + ":Link/Designation:200",
		_("Department") + ":Link/Department:200",
		_("Salary Slip") + ":Link/Salary Slip:100",
		_("Present Days") + ":Data:100",
		_("Total Days") + ":Data:100",
		_("Total OT Hours") + ":Float:100",
		_("Rate of Wages") + ":Currency:100",
		_("Shift Wages") + ":Currency:100",
		_("OT Wages") + ":Currency:100",
		_("Gross Wages") + ":Currency:100",
		_("PF") + ":Currency:100",
		_("ESI") + ":Currency:100",
		_("Total Deductions") + ":Currency:100",
		_("Net Wages") + ":Currency:100",
		]
	
	return columns
