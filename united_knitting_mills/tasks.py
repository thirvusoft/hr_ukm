import frappe
import datetime

@frappe.whitelist()
def all():
    doc_list = frappe.get_all('Employee Checkin', ['employee', 'time', 'name'])
    date_format_str = '%Y-%m-%d %H:%M:%S'
    count = 0
    doc_len = len(doc_list)
    for doc in doc_list:
        count += 1
        try:
            check = frappe.db.sql('''select name from `tabEmployee Checkin` where employee = '{0}' and time between '{1}' and '{2}' '''.format(doc.get('employee') , datetime.datetime.strptime(str(doc.get('time')), date_format_str) , datetime.datetime.strptime(str(doc.get('time')), date_format_str) + datetime.timedelta(minutes = 2) ),as_list=1)
            if(len(check)>1):
                exists = frappe.get_all(
                        "Checkin test",
                        filters={"message": ("like", "{0}%".format(check))},
                        as_list=1,
                    )            
                if not exists:
                    doc = frappe.new_doc('Checkin test')
                    doc.update({
                        'docname': doc.get('name'),
                        'employee': doc.get('employee'),
                        'message': str(check)
                    })
                    doc.save()
        except Exception as e:
            doc = frappe.new_doc('Checkin test')
            doc.update({
                'docname': doc.get('name'),
                'employee': doc.get('employee'),
                'message': str(e)+ ' ' + str(type(e)) + str(frappe.get_traceback())
            })
            doc.save()
    frappe.db.commit()
    return "TEST"