# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
 
def execute(filters=None):
    attendance_date = filters.get("attendance_date")
    designation = filters.get("designation")
    conditions = ""
    if attendance_date or designation:
        conditions = " where docstatus = 1"
        if attendance_date :
            conditions += "  and attendance_date = '{0}' ".format(attendance_date)
        if designation:
            conditions += " and designation = '{0}' ".format(designation)

            
    report_data = frappe.db.sql(""" select
    							designation,
                                name,
                                employee,
                                employee_name,
                                checkin_time,
                                checkout_time,
                                late_min,
                                total_shift_count
                                from `tabAttendance`
                                {0} order by designation
                                """.format(conditions))


    data = [list(i) for i in report_data]

    check =''
    for i in range (0,len(data),1):
        if data[i][0] != check:
            if i<len(data)-1: check = data[i+1][0] 
            data[i][0] = f'<b>{data[i][0]}</b>'

        else:
            data[i][0]=''
    columns = get_columns()
    return columns, data
 
def get_columns():
    columns = [
        _("Designation") + ":Data:100",
        _("Name") + ":Link/Attendance:200",
        _("Employee Code") + ":Link/Employee:200",
        _("Employee Name") + ":Data:200",
        _("In-Time") + ":Time:100",
        _("Out-Time") + ":Time:100",
        _("Late Entry in Minutes") + ":Data:200",
        _("Total Shift") + ":Float:100",
        ]
    
    return columns
