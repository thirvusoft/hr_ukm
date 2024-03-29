import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def create_employee_fields_and_property_setter():
    custom_fields = {
        "Employee": [
            dict(fieldname='location', label='Location',
                fieldtype='Link',options='Location', insert_after='last_name', read_only=0,reqd=1),
            dict(fieldname='abbr', label='Abbreviation',
                fieldtype='Data', insert_after='location', hidden=1,fetch_from='location.abbr'),
            dict(fieldname='enable_esi', label='Enable ESI',
                fieldtype='Check', insert_after='date_of_joining', hidden=1),
            dict(fieldname='enable_pf', label='Enable PF',
                fieldtype='Check', insert_after='enable_esi', hidden=1),
            dict(fieldname='hr_permission', label='HR Permission',
                fieldtype='Check', insert_after='location', hidden=1), 
            dict(fieldname='approval_by_owner', label='Approved By Owner',
                fieldtype='Check', insert_after='company', hidden=1),
            dict(fieldname='ts_column_break_1',
                fieldtype='Column Break', insert_after='payroll_cost_center'),
            dict(fieldname='ts_column_break_2',
                fieldtype='Column Break', insert_after='marital_status'),
            dict(fieldname='ts_column_break_3',
                fieldtype='Column Break', insert_after='department'),
            dict(fieldname='ts_column_break_4',
                fieldtype='Column Break', insert_after='emergency_phone_number'),
            dict(fieldname='relationship', label='Relationship',
                fieldtype='Link', insert_after='ts_column_break_4', options='Relationship'),
            dict(fieldname='ts_sec_brk_111', label='Interview Details',
                fieldtype='Section Break', insert_after='date_of_joining'),
            dict(fieldname='ts_interview_details',
                fieldtype='Table', insert_after='ts_sec_brk_111', options='TS INTERVIEW DETAILS'),
            dict(fieldname='add_html',
                fieldtype='Small Text', insert_after='current_address'),
            dict(fieldname='ts_bank_branch_name', label='Branch Name',
                fieldtype='Link', insert_after='bank_name', options='Territory', depends_on = "eval:doc.salary_mode == 'Bank'", read_only_depends_on ="eval:!doc.__islocal")
        ]
    }

    create_custom_fields(custom_fields)
    
    ## Property Setter
    make_property_setter("Employee", "naming_series", "default", "employee_naming_series.-.####", "Select")
    make_property_setter("Employee", "naming_series", "hidden", 1, "Select")
    make_property_setter("Employee", "attendance_device_id", "read_only", 1, "Select")
    make_property_setter("Employee", "emergency_contact_details", "collapsible", 1, "Section Break")
    make_property_setter("Employee", "company", "default", "United Knitting Mills", "Text")
    make_property_setter("Employee", "company", "hidden", 1, "Check")
    make_property_setter("Employee", "branch", "hidden", 1, "Check")
    make_property_setter("Employee", "approvers_section", "hidden", 1, "Section Break")
    make_property_setter("Employee", "default_shift", "hidden", 1, "Check")
    make_property_setter("Employee", "unsubscribed", "hidden", 1, "Check")
    make_property_setter("Employee", "leave_encashed", "hidden", 1, "Check")
    make_property_setter("Employee", "create_user", "hidden", 1, "Button")
    make_property_setter("Employee", "employment_details", "hidden", 1, "Section Break")
    make_property_setter("Employee", "erpnext_user", "hidden", 1, "Section Break")
    make_property_setter("Employee", "holiday_list", "reqd", 1, "Check")

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"middle_name",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"salutation",
        "value":1
    })
    employee.save(ignore_permissions=True) 

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"grade",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"employment_type",
        "value":1
    })
    employee.save(ignore_permissions=True)
    
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"reports_to",
        "value":1
    })
    employee.save(ignore_permissions=True)
    
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sb53",
        "value":1
    })
    employee.save(ignore_permissions=True)

    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"label",
        'property_type':"Section Break",
        'field_name':"erpnext_user",
        "value":"Thirvu User"
    })
    employee.save(ignore_permissions=True)
    
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"relation",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"unsubscribed",
        "value":1
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"passport_number",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"date_of_issue",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"valid_upto",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"place_of_issue",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"family_background",
        "value":1
    })
    employee.save(ignore_permissions=True)
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"health_details",
        "value":1
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"default",
        'property_type':"text",
        'field_name':"salary_mode",
        "value":"Bank"
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"read_only_depends_on",
        'property_type':"text",
        'field_name':"bank_name",
        "value":"eval:!doc.__islocal"
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"read_only_depends_on",
        'property_type':"text",
        'field_name':"bank_ac_no",
        "value":"eval:!doc.__islocal"
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"read_only_depends_on",
        'property_type':"text",
        'field_name':"ifsc_code",
        "value":"eval:!doc.__islocal"
    })
    employee=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Employee",
        'property':"read_only_depends_on",
        'property_type':"text",
        'field_name':"micr_code",
        "value":"eval:!doc.__islocal"
    })
    employee.save(ignore_permissions=True)
    create_custom_fields(custom_fields)