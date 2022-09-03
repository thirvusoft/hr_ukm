import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    

def location():
    custom_fields = {
		"Location": [
            dict(fieldname='current_series', label='Current Series',
				fieldtype='Int', insert_after='cb_details',default='1',hidden=1),
            dict(fieldname='naming_series', label='Employee Naming Series',
				fieldtype='Data', insert_after='current_series',hidden=0,),    
		],
    }
    create_custom_fields(custom_fields)
def sequence_user_id(doc,event):
        try:
            if doc.__islocal == 1 :
                last_doc = frappe.get_last_doc("Location", {"location": doc.location})
                doc.current_series = int(last_doc.current_series) + 1
        except:
            pass
def autoname(self, event):
	self.naming_series= "UKM"+ " " +str(self.current_series)

    