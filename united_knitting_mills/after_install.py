from united_knitting_mills.ukm.custom_fields.hr.employee import create_employee_fields_and_property_setter
from united_knitting_mills.ukm.custom_fields.hr.leave_application import leave_application_customizations
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
from united_knitting_mills.ukm.custom_fields.hr.employee_checkin import checkin_customisation
from united_knitting_mills.ukm.utils.python.defaults import create_defults
from united_knitting_mills.ukm.custom_fields.hr.holiday_list import holiday_list_customisation
from united_knitting_mills.ukm.custom_fields.hr.salary_structure import salary_structure_customizations
from united_knitting_mills.ukm.custom_fields.hr.salary_structure_assignment import salary_structure_assignment_customizations
from united_knitting_mills.ukm.custom_fields.hr.payroll_entry import payroll_entry_customizations
from united_knitting_mills.ukm.custom_fields.hr.salary_slip import salary_slip_customizations
from united_knitting_mills.ukm.custom_fields.hr.employee_advance import employee_advance_customisation

def create_custom_fields():
    leave_application_customizations()
    create_defults()
    attendance_customisation()
    create_company_fields()
    create_employee_fields_and_property_setter()
    create_payroll_settings_fields()
    create_shift_type_fields()
    department_customisation()
    create_location_fields()
    employee_bonus_tool_custom_fields()
    bonus_percentage_fields()
    workflow_document_creation()
    assignment_workflow_document_creation()
    employee_custom_field()
    location()
    designation_customisation()
    checkin_customisation()
    holiday_list_customisation()
    salary_structure_customizations()
    salary_structure_assignment_customizations()
    payroll_entry_customizations()
    salary_slip_customizations()
    employee_advance_customisation()