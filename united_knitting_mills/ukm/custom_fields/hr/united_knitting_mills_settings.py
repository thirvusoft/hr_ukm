from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def bonus_percentage_fields():
    custom_fields = {
		"United Knitting Mills Settings": [
			dict(fieldname='SB1', 
				fieldtype='Section Break',insert_after='ts_create'),
			dict(fieldname='bonus_percentage', label='Bonus Percentage',
				fieldtype='Percent',insert_after='SB1',reqd=1)
        ]}
    
    create_custom_fields(custom_fields)
          


          