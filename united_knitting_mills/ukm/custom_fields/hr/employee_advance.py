import frappe

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def employee_advance_customisation():
    employee_advance_custom_fields()
    employee_advance_property_setter()

def employee_advance_custom_fields():

    custom_fields = {

		"Employee Advance": [
            
            dict(fieldname = 'location', 
                label = 'Location',
				fieldtype = 'Link',
                options = 'Location',
                insert_after = 'mode_of_payment',
                fetch_from = 'employee.location'
            ),

            dict(fieldname = 'eligible_amount', 
                label = 'Eligible Amount',
				fieldtype = 'Currency',
                insert_after = 'column_break_11',
                read_only = 1
            ),

            dict(fieldname = 'reference_document', 
                label = 'Reference Document',
				fieldtype = 'Link', 
                insert_after = 'purpose', 
                read_only = 1,
                options = "Employee Advance Tool"
            ),

            dict(fieldname = 'from_date', 
                label = 'From Date',
				fieldtype = 'Date', 
                insert_after = 'posting_date', 
                read_only = 1
            ),

            dict(fieldname = 'to_date', 
                label = 'To Date',
				fieldtype = 'Date', 
                insert_after = 'from_date', 
                read_only = 1
            ),

            dict(fieldname = 'total_shift', 
                label = 'Total Shift',
				fieldtype = 'Float', 
                insert_after = 'advance_amount', 
                read_only = 1
            ),

            dict(fieldname = 'designation', 
                label = 'Designation',
				fieldtype = 'Link', 
                insert_after = 'department', 
                read_only = 1,
                options = "Designation",
                fetch_from = "employee.designation"
            ),

            dict(fieldname = 'location', 
                label = 'Location',
				fieldtype = 'Link', 
                insert_after = 'designation', 
                read_only = 1,
                options = "Location",
                fetch_from = "employee.location"
            ),
             dict(fieldname = 'is_hold', 
                label = 'Is Hold',
				fieldtype = 'Check', 
                insert_after = 'location', 
            ),
        ]
    }
    create_custom_fields(custom_fields)

def employee_advance_property_setter():

    defaults = frappe.get_single("Global Defaults")
    company = defaults.default_company
    company_doc = frappe.get_doc("Company",company)
    abbr = company_doc.abbr
    currency = company_doc.default_currency

    if not frappe.db.exists("Account", {"account_name": "Employee Advance", "company": company}):
        emp_advance_account = frappe.new_doc("Account")
        emp_advance_account.account_name = "Employee Advance"
        emp_advance_account.company = company
        emp_advance_account.parent_account = f"Cash In Hand - {abbr}"
        emp_advance_account.root_type = "Asset"
        emp_advance_account.report_type = "Balance Sheet"
        emp_advance_account.account_currency = currency
        emp_advance_account.save()
        
    advance_account=frappe.db.get_value("Account",{"account_name":"Employee Advance","company":company},"name")
    
    make_property_setter("Employee Advance", "company", "default",company,"Small Text")
    make_property_setter("Employee Advance", "posting_date", "read_only", 1, "Check")
    make_property_setter("Employee Advance", "repay_unclaimed_amount_from_salary", "default", 1, "Check")
    make_property_setter("Employee Advance", "advance_account", "default",advance_account, "Small Text")
    make_property_setter("Employee Advance", "repay_unclaimed_amount_from_salary", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "status", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "company", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "paid_amount", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "pending_amount", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "claimed_amount", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "return_amount", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "currency", "default",currency, "Small Text")
    make_property_setter("Employee Advance", "currency", "hidden", 1, "Check")
    make_property_setter("Employee Advance", "exchange_rate", "default","1", "Small Text")
    make_property_setter("Employee Advance", "exchange_rate", "hidden",1, "Check")
    make_property_setter("Employee Advance", "status", "options","Draft\nPaid\nUnpaid\nClaimed\nReturned\nPartly Claimed and Returned\nCancelled\nApproved","Small Text")
    make_property_setter("Employee Advance", "status", "allow_on_submit",1,"Check")
    make_property_setter("Employee Advance", "naming_series", "default","HR-EAD-.YYYY.-", "Small Text")
    make_property_setter("Employee Advance", "naming_series", "hidden", 1, "Check")