from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_shift_type_fields():
    custom_fields = {
		"Shift Type": [
			dict(fieldname='location', label='Location',
				fieldtype='Link',options='Location',insert_after='holiday_list',reqd=1),
			dict(fieldname='abbr', label='Abbr',
				fieldtype='Data', fetch_from='location.abbr',insert_after='location'),
            dict(fieldname='working_hours_threshold_for_quater_day', label='Working Hours Threshold for Quarter Day',
				fieldtype='Float',insert_after='working_hours_threshold_for_half_day'),
            dict(fieldname='working_hours_threshold_for_three_quarter_day', label='Working Hours Threshold for Three Quarter Day',
				fieldtype='Float',insert_after='working_hours_threshold_for_quater_day'),
            dict(fieldname='working_hours_threshold_for_one_quarter_day', label='Working Hours Threshold for One Quarter Day',
				fieldtype='Float',insert_after='working_hours_threshold_for_three_quarter_day'),
            dict(fieldname='working_hours_threshold_for_one_half_day', label='Working Hours Threshold for One Half Day',
				fieldtype='Float',insert_after='working_hours_threshold_for_one_quarter_day'),
            ]
    }
    create_custom_fields(custom_fields)