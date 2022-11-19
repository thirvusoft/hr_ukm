import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_slip_customizations():
    salary_slip_property_setter()
    salary_slip_custom_fields()

def salary_slip_property_setter():
    make_property_setter("Salary Slip", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Salary Slip", "company", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "currency", "default", "INR", "Text")
    make_property_setter("Salary Slip", "currency", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "status", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "letter_head", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "salary_slip_based_on_timesheet", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "section_break_32", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "loan_repayment", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "section_break_43", "hidden", 1, "Check")
    make_property_setter("Salary Slip", "leave_without_pay", "hidden", 1, "Check")

def salary_slip_custom_fields():
    custom_fields = {
		"Salary Slip": [
			dict(fieldname='total_shift_worked', label='Total Shift Worked',
         fieldtype='Data', insert_after='total_working_days',read_only=1),
         dict(fieldname='total_shift_minutes', label='Total Shift in Minutes',
         fieldtype='Data', insert_after='total_shift_worked',read_only=1),
         dict(fieldname='extra_minutes', label='Extra Shift in Minutes',
         fieldtype='Data', insert_after='total_shift_minutes',read_only=1),
         dict(fieldname='ts_shift_amount', label='Shift amount',
         fieldtype='Currency', insert_after='extra_minutes',hidden=1),
         dict(fieldname="is_staff_calulation", label='Is Staff Calulation',
         fieldtype='Check', insert_after='ts_shift_amount',hidden=1),
         dict(fieldname="per_day_salary_for_staff", label='Per Day Salary For Staff',
         fieldtype='Float', insert_after='is_staff_calulation',hidden=1),
         dict(fieldname='ts_column_break',
         fieldtype='Column Break',insert_after='employee'),
         dict(fieldname='leave_with_pay', label='Leave With Pay',
         fieldtype='Int', insert_after='leave_without_pay',read_only=1),
        ]
    }
    create_custom_fields(custom_fields)