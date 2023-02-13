from ctypes.wintypes import PFLOAT
import frappe
import pandas
from datetime import date, datetime, timedelta
from frappe import _
from erpnext.education.report.student_monthly_attendance_sheet.student_monthly_attendance_sheet import daterange
from frappe.utils.data import date_diff
from erpnext.hr.utils import get_holiday_dates_for_employee

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	frappe.publish_realtime('refresh-report')
	return columns, data

def get_columns(filters):
	columns = [
		 {
			"label": _("S.No"),
			"fieldtype": "Data",
			"fieldname": "sno",
			"width": 50
		},
		{
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"fieldname": "code",
			"options":"Employee",
			"width": 110
		},
		{
			"label": _("Name of Employee"),
			"fieldtype": "Data",
			"fieldname": "worker_name",
			"width": 100
		},
		{
			"label": _("Designation"),
			"fieldtype": "Data",
			"fieldname": "designation",
			"width": 100
		},
		
		]
	from_date = filters["from_date"]
	to_date = filters["to_date"]
	from_d = tuple(map(int, from_date.split('-')))
	to_d = tuple(map(int, to_date.split('-')))
	between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
	for i in between_dates:
		
		columns.append({

			"label": i[len(i)-2:],
			"fieldtype": "Data",
			"fieldname": i,
			"width": 70,
		}),
  

	columns+=[

		{
			"label": _("Gross Salary"),
			"fieldtype": "Data",
			"fieldname": "gross_salary",
			"width": 110
		},
		{
			"label": _("Per-Day Salary"),
			"fieldtype": "Data",
			"fieldname": "per_day_salary",
			"width": 120
		},
		{
			"label": _("Present Days"),
			"fieldtype": "Data",
			"fieldname": "present_days",
			"width": 120
		},
		{
			"label": _("Absent Days"),
			"fieldtype": "Data",
			"fieldname": "absent_days",
			"width": 120
		},
		{
			"label": _("Worked Sundays"),
			"fieldtype": "Data",
			"fieldname": "worked_sundays",
			"width": 130
		},
		{
			"label": _("Net Salary"),
			"fieldtype": "Data",
			"fieldname": "total_shift_amount",
			"width": 100
		}
	   
	]
	return columns
def get_data(filters):
	data=[]
	from_date = filters["from_date"]
	to_date = filters["to_date"]

	filter = {'attendance_date':["between", (from_date, to_date)],'docstatus':1}
	
	keys = list(filters.keys())

	from_d = tuple(map(int, from_date.split('-')))
	to_d = tuple(map(int, to_date.split('-')))

	between_dates = list(map(str, list(daterange(date(from_d[0], from_d[1], from_d[2]),date(to_d[0], to_d[1], to_d[2])))))
   
	if ("designation" in keys):
		filter["designation"] = filters["designation"]

	if ("department" in keys):
		filter["department"] = filters["department"]

	if ("unit" in keys):
		filter["unit"] = filters["unit"]

	attendance=frappe.db.get_all("Attendance", filters=filter, fields=["name","employee","employee_name","designation","unit", "total_shift_count", "total_shift_amount" ], 
	group_by="employee",
	order_by="designation")
	no=1
	for j in attendance:
		f=frappe._dict()
		out=frappe._dict()
		tot = frappe._dict()
		f.update(
			{   "sno":str(no),
				"code" : j['employee'],
				"worker_name":j.employee_name,
				"designation" : j.designation,
				
			}
		)
		shift=0
		shift_amount=0
		sunday = 0
		for k in between_dates:
			get_attendance=frappe.db.get_list("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, ['checkin_time','checkout_time','total_shift_count'])
			get_amount=frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'total_shift_amount')
			sunday_attendance=frappe.db.get_value("Attendance", {'employee':j.employee, 'workflow_state':"Present",'attendance_date':k}, 'sunday_attendance')
			if sunday_attendance:
				sunday += 1
			if get_attendance:
				checkin = get_attendance[0]['checkin_time']
				checkout = get_attendance[0]['checkout_time']
				f.update({k:f'{checkin or "-"}'})
				out.update({k:f'{checkout or "-"}'})
				tot.update({k:f"<span style='color:green!important;font-weight:bold'>{get_attendance[0]['total_shift_count']}</span>"})
				shift=shift+(get_attendance[0]['total_shift_count'] or 0)
			else:
				f.update({k:"-"})
				out.update({k:"-"})
				tot.update({k:f"<span style='color:red!important;font-weight:bold'>0</span>"})

		
		payment_days = date_diff(to_date, from_date) + 1
		holidays = get_holiday_dates_for_employee(j.employee,from_date, to_date)
		payment_days -= len(holidays)
		emp_base_amount = frappe.get_value("Salary Structure Assignment",{"employee":j.employee,"docstatus":1},["base"])
		
		if emp_base_amount:
			shift_amount = (emp_base_amount/payment_days) * shift
		else:
			emp_base_amount = 0
		tot.update({"gross_salary":f'<b>{emp_base_amount}</b>',"per_day_salary":f'<b>{round((emp_base_amount/payment_days),2) or 0}</b>',"present_days":f'<b>{shift}</b>',"absent_days":f'<b>{payment_days-shift}</b>',"worked_sundays":f'<b>{sunday}</b>',"total_shift_amount":f'<b>{round(shift_amount,2)}</b>'})

		data.append(f)
		data.append(out)
		data.append(tot)
		no+=1   
	return data

