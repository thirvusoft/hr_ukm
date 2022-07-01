import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_employee_fields_and_property_setter():
    custom_fields = {
        "Employee": [
            dict(fieldname='location', label='Location',
                fieldtype='Link',options='Location', insert_after='last_name', read_only=0),
            dict(fieldname='abbr', label='Abbreviation',
                fieldtype='Data', insert_after='location', hidden=1,fetch_from='location.abbr'),
            dict(fieldname='enable_esi', label='Enable ESI',
                fieldtype='Check', insert_after='date_of_joining', hidden=1),
            dict(fieldname='enable_pf', label='Enable PF',
                fieldtype='Check', insert_after='enable_esi', hidden=1),
        ]
    }


    ## Property Setter
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
    employee.save(ignore_permissions=True)
    create_custom_fields(custom_fields)