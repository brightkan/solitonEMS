from django.contrib.auth import get_user_model
import datetime

from employees.models import Employee
from organisation_details.selectors import get_department_instance
from .models import LeaveApplication, LeaveRecord, Leave_Types, LeavePlan

user = get_user_model()


# Leave Type Selectors
def get_all_leave_types():
    return Leave_Types.objects.all()


def get_leave_type(leave_type_id):
    return Leave_Types.objects.get(pk=leave_type_id)


# Leave Records Selectors
def get_all_leave_records():
    return LeaveRecord.objects.all()


def get_leave_record(employee, year):
    try:
        leave_record = LeaveRecord.objects.get(employee=employee, leave_year=year)
        return leave_record
    except LeaveRecord.DoesNotExist:
        return None


# Leave Application Selectors
def get_all_leave_applications():
    return LeaveApplication.objects.all()


def get_employee_leave_applications(employee):
    return LeaveApplication.objects.filter(employee=employee)


def get_employee_leave_details(employee, leave_year):
    leave_applications = LeaveApplication.objects.filter(employee=employee, apply_date__year=leave_year)

    return leave_applications


def get_leave_application(leave_application_id):
    return LeaveApplication.objects.get(pk=leave_application_id)


def get_supervisor_users(applicant):
    team = applicant.team

    all_supervisor_users = user.objects.filter(is_supervisor=True)
    users = []
    for supervisor_user in all_supervisor_users:
        if supervisor_user.solitonuser.employee.team == team:
            users.append(supervisor_user)

    return users


def get_hod_users(applicant):
    department = applicant.department
    all_hod_users = user.objects.filter(is_hod=True)
    users = []
    for hod_user in all_hod_users:
        if hod_user.solitonuser.employee.department == department:
            users.append(hod_user)
    return users


def get_hr_users():
    all_hr_users = user.objects.filter(is_hr=True)
    return all_hr_users


def get_recent_leave_plans(limit, employee):
    return LeavePlan.objects.filter(employee=employee).order_by('-id')[:limit]


def get_hod_pending_leave_plans(hod):
    pending_leave_plans = LeavePlan.objects.filter(approval_status="Pending")
    hod_department = get_department_instance(hod)
    hod_pending_applications = []
    for pending_leave_plan in pending_leave_plans:
        applicant = pending_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_pending_applications.append(pending_leave_plan)
    return hod_pending_applications


def get_leave_plan(id):
    return LeavePlan.objects.get(id=id)


def get_approved_leave_plans(hod: Employee, month: int):
    approved_leave_plans = LeavePlan.objects.filter(approval_status="Approved", start_date__month=month)
    hod_department = get_department_instance(hod)
    hod_approved_applications = []
    for approved_leave_plan in approved_leave_plans:
        applicant = approved_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_approved_applications.append(approved_leave_plan)
    return hod_approved_applications


def get_hod_approved_leave_plans(hod):
    approved_leave_plans = LeavePlan.objects.filter(approval_status="Approved")
    hod_department = get_department_instance(hod)
    hod_approved_applications = []
    for approved_leave_plan in approved_leave_plans:
        applicant = approved_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_approved_applications.append(approved_leave_plan)
    return hod_approved_applications


def get_current_year():
    return datetime.datetime.now().year


def get_all_non_expired_leave_plan_applications():
    leave_plan_applications = LeavePlan.objects.filter(expired=False, approval_status="Pending")
    return leave_plan_applications


def get_all_non_expired_leave_applications():
    leave_applications = LeaveApplication.objects.filter(expired=False, overall_status="Pending")
    return leave_applications
