from united_knitting_mills.ukm.custom_fields.hr.employee import create_employee_fields
from united_knitting_mills.ukm.custom_fields.payroll.payroll_entry import create_payroll_entry_fields
from united_knitting_mills.ukm.custom_fields.payroll.salary_slip import create_salary_slip_fields
from united_knitting_mills.ukm.custom_fields.payroll.salary_structure import create_salary_structure_fields
from united_knitting_mills.ukm.custom_fields.hr.company import create_company_fields
from united_knitting_mills.ukm.custom_fields.hr.shift_type import create_shift_type_fields
from united_knitting_mills.ukm.custom_fields.payroll.payroll_settings import create_payroll_settings_fields

def create_custom_fields():
    create_company_fields()
    create_employee_fields()
    create_payroll_entry_fields()
    create_payroll_settings_fields()
    create_salary_slip_fields()
    create_salary_structure_fields()
    create_shift_type_fields()