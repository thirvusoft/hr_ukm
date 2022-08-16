from united_knitting_mills.ukm.custom_fields.hr.employee import create_employee_fields_and_property_setter
from united_knitting_mills.ukm.custom_fields.payroll.payroll_entry import create_payroll_entry_fields
from united_knitting_mills.ukm.custom_fields.payroll.salary_slip import create_salary_slip_fields
from united_knitting_mills.ukm.custom_fields.payroll.salary_structure import create_salary_structure_fields
from united_knitting_mills.ukm.custom_fields.hr.company import create_company_fields
from united_knitting_mills.ukm.custom_fields.hr.shift_type import create_shift_type_fields
from united_knitting_mills.ukm.custom_fields.payroll.payroll_settings import create_payroll_settings_fields
from united_knitting_mills.ukm.custom_fields.hr.attendance import attendance_customisation
from united_knitting_mills.ukm.custom_fields.assets.location import create_location_fields
from united_knitting_mills.ukm.custom_fields.hr.employee_bonus_tool import employee_bonus_tool_custom_fields
from united_knitting_mills.ukm.custom_fields.hr.united_knitting_mills_settings import bonus_percentage_fields
from united_knitting_mills.ukm.utils.python.workflow import workflow_document_creation
from united_knitting_mills.ukm.utils.python.salary_assignment_workflow import assignment_workflow_document_creation
from united_knitting_mills.ukm.custom_fields.hr.department import department_customisation
from united_knitting_mills.ukm.utils.python.employee import employee_custom_field
from united_knitting_mills.ukm.utils.python.location import location
from united_knitting_mills.ukm.custom_fields.hr.designation import designation_customisation


def create_custom_fields():
    create_company_fields()
    create_employee_fields_and_property_setter()
    create_payroll_entry_fields()
    create_payroll_settings_fields()
    create_salary_slip_fields()
    create_salary_structure_fields()
    create_shift_type_fields()
    attendance_customisation()
    department_customisation()
    create_location_fields()
    employee_bonus_tool_custom_fields()
    bonus_percentage_fields()
    workflow_document_creation()
    assignment_workflow_document_creation()
    employee_custom_field()
    location()
    designation_customisation()