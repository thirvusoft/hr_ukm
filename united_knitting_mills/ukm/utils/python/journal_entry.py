import frappe
@frappe.whitelist()
def get_user_location(user):
    location=[]
    location_list = frappe.db.sql('''select parent from `tabThirvu Location User` where user = '{0}' '''.format(user),as_list=1)
    for data in location_list:
        location.append(data[0])
    return location