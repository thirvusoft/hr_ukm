import frappe
from frappe.utils import nowdate,add_days
def validate_to_date(doc,event):

    if (doc.end_date >= nowdate()):
        doc.end_date = add_days(nowdate(),-1)
        frappe.msgprint(f'End Date cannot be greater than Yesterday ({doc.end_date}). Valid date is applied.')

@frappe.whitelist()
def get_start_end_dates(payroll_frequency, start_date=None, company=None):
    pass