# Copyright (c) 2023, UKM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import  add_days

class EmployeeSalaryDetails(Document):
    def validate(self):
        date_validate = frappe.db.sql(f'''
                                    SELECT name
                                    FROM `tabEmployee Salary Details` esd
                                    WHERE  ('{self.from_date}' between esd.from_date and esd.to_date
           								OR '{self.to_date}' between esd.from_date and esd.to_date)
										AND esd.employee = '{self.employee}'
          								AND esd.docstatus = 1
                                      ''', as_dict=1)
        if date_validate:
            frappe.throw(f"This Employee Already have Base of {self.from_date} to {self.to_date}")
    def on_submit(self):
        esd_details = frappe.db.get_list("Employee Salary Details", {"employee":self.employee, "from_date": ["<", self.from_date], "to_date":["is", "not set"] })
        if esd_details:
            frappe.db.set_value("Employee Salary Details", esd_details[0], "to_date", add_days(self.from_date, -1)
        )   