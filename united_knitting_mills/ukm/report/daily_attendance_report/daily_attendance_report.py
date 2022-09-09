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
                                name,
                                employee,
                                employee_name,
                                checkin_time,
                                checkout_time,
								designation,
                                late_min,
                                total_shift_count
                                from `tabAttendance`
                                {0} order by designation
                                """.format(conditions))

    designation_count = frappe.db.sql(""" select
                                count(*)
                                from `tabAttendance`
                                where docstatus = 1 and attendance_date = '{0}' group by designation
                                """.format(attendance_date))

    data = [list(i) for i in report_data]
    matched_item=""
    index = 0
    if data[0][5]:
        check = data[0][5]

    for i in range (0,(len(data)+len(designation_count))-1,1):
        if data[i][5] != check:
            check = data[i][5]
            data.insert(i,[f'<b>{check}</b>','','','','','','',''])

    columns = get_columns()
    return columns, data
 
def get_columns():
    columns = [
        _("Name") + ":Link/Attendance:200",
        _("Employee Code") + ":Link/Employee:200",
        _("Employee Name") + ":Data:200",
        _("In-Time") + ":Time:100",
        _("Out-Time") + ":Time:100",
        _("Designation") + ":Link/Designation:100",
        _("Late Entry Minutes") + ":Data:200",
        _("Total Shift") + ":Float:100",
        ]
    
    return columns
