# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt
 
import frappe
from frappe import _
 
def execute(filters=None):
    attendance_date = filters.get("attendance_date")
    designation = filters.get("designation")
    staff_labour = filters.get("staff_or_labour")
    unit =  filters.get("unit")
    conditions = ""
    if attendance_date or designation or staff_labour or unit:
        conditions = " where 1 = 1"
        if attendance_date :
            conditions += "  and attendance_date = '{0}' ".format(attendance_date)
        if designation:
            conditions += " and designation = '{0}' ".format(designation)
        if staff_labour and staff_labour=='Staff':
            conditions += ' and staff = 1'
        elif staff_labour and staff_labour=='Labour':
            conditions += ' and staff = 0'
        if unit:
            conditions += ' and unit = "{0}" '.format(unit)
            
            
    report_data = frappe.db.sql("""SELECT DISTINCT
                                    att.designation,
                                    att.employee,
                                    att.employee_name,
                                    att.checkin_time,
                                    att.checkout_time,
                                    att.late_min,
                                    att.total_shift_count,
                                    att.total_shift_amount,
                                    doc.check_in_time,
                                    doc.check_out_time
                                FROM `tabAttendance` AS att
                                LEFT OUTER JOIN `tabThirvu Employee Checkin Details` AS doc ON doc.parent = att.name
                                {0}
                                ORDER BY att.designation
                                """.format(conditions))



    data = [list(i) for i in report_data]

    check =''
    for i in range (0,len(data),1):
        if data[i][0] != check:
            check = data[i][0] 
            data[i][0] = f'<b>{data[i][0]}</b>'

        else:
            data[i][0]=''
        if data[i][8]:
            data[i][3] = data[i][8]
        if data[i][9]:
            data[i][4] = data[i][9]
    columns = get_columns()
    return columns, data
 
def get_columns():
    columns = [
        _("Designation") + ":Data:200",
        _("Employee Code") + ":Link/Employee:200",
        _("Employee Name") + ":Data:200",
        _("In-Time") + ":Time:100",
        _("Out-Time") + ":Time:100",
        _("Late Entry in Minutes") + ":Data:160",
        _("Total Shift") + ":Float:100",
        _("Wages") + ":Float:100",
        ]
    
    return columns
