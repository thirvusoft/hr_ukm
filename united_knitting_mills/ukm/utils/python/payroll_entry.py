import frappe
from frappe.utils import nowdate,add_days
def validate_to_date(doc,event):
    if (doc.end_date >= nowdate()):
        pass
        # doc.end_date = add_days(nowdate(),-1)
        # frappe.msgprint(f'End Date cannot be greater than Yesterday ({doc.end_date}). Valid date is applied.')
