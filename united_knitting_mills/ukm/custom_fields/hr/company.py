from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_company_fields():
    custom_fields = {
		"Company": [
			dict(fieldname='compliance_and_audit', label='Compliance and audit',
				fieldtype='Check',default=0, insert_after='is_group'),
			dict(fieldname='ts_company_name', label='Company Name',
				fieldtype='Link',options='Company', depends_on='eval:doc.compliance_and_audit==1',mandatory_depends_on='eval:doc.compliance_and_audit==1',insert_after='compliance_and_audit'),
            ]
    }
    create_custom_fields(custom_fields)