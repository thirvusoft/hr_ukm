import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def employee_bonus_tool_custom_fields():
          custom_fields = {
          "Employee Bonus Tool":[
                    # dict(
                    #           fieldname='CB',
                    #           fieldtype='Column Break', 
                    #           insert_after='designation',
                              
                    # ),
                    dict(
                              fieldname='from_date', 
                              label='From Date',
                              fieldtype='Date', 
                              insert_after='date',
                              reqd=1
                              
                    ),
                    dict(
                              fieldname='to_date', 
                              label='To Date',
                              fieldtype='Date', 
                              insert_after='from_date',
                                     reqd=1
                             
                    ),
                    dict(
                              fieldname='SB1',
                              fieldtype='Section Break', 
                              insert_after='designation',
                              
                    ),
          ],}
          create_custom_fields(custom_fields)




   