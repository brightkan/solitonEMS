from django.contrib.auth import get_user_model
import datetime
from employees.models import Employee
from organisation_details.selectors import get_team_instance, get_is_supervisor_in_team, \
    get_is_hod_in_department
from overtime.models import OvertimeApplication, OvertimePlan, OvertimeSchedule

User = get_user_model()


def get_overtime_application(id):
    return OvertimeApplication.objects.get(pk=id)


def get_hod_pending_overtime_applications(hod_department):
    # Get the pending overtime applications for the particular hod department
    pending_applications = OvertimeApplication.objects.filter(status="Pending", HOD_approval="Pending",
                                                              supervisor_approval="Approved")

    hod_pending_applications = []
    for pending_application in pending_applications:
        if pending_application.applicant.department == hod_department:
            hod_pending_applications.append(pending_application)
    return hod_pending_applications


def get_hod_approved_overtime_applications(user):
    hod_department = user.solitonuser.employee.department
    # Get the approved overtime applications for the particular hod department
    approved_applications = OvertimeApplication.objects.filter(status="Pending", HOD_approval="Approved")
    hod_pending_applications = []
    for approved_application in approved_applications:
        if approved_application.supervisee.department == hod_department:
            hod_pending_applications.append(approved_application)
    return hod_pending_applications


def get_cfo_pending_overtime_applications():
    pending_applications = OvertimeApplication.objects.filter(status="Pending", cfo_approval="Pending",
                                                              HOD_approval="Approved")
    return pending_applications


def get_ceo_pending_overtime_applications():
    pending_applications = OvertimeApplication.objects.filter(status="Pending", cfo_approval="Approved",
                                                              ceo_approval="Pending")

    return pending_applications


def get_approved_overtime_applications(employee: Employee):
    approved_applications = OvertimeApplication.objects.filter(status="Approved", applicant=employee)
    return approved_applications


def get_all_overtime_applications():
    overtime_applications = OvertimeApplication.objects.all()
    return overtime_applications


def get_supervisor_pending_overtime_applications(supervisor):
    pending_applications = OvertimeApplication.objects.filter(supervisor_approval="Pending")
    supervisor_team = get_team_instance(supervisor)
    supervisor_pending_applications = []
    for pending_application in pending_applications:
        applicant = pending_application.applicant
        applicant_team = get_team_instance(applicant)
        if applicant_team.id is supervisor_team.id:
            supervisor_pending_applications.append(pending_application)
    return supervisor_pending_applications


def get_hr_pending_overtime_applications():
    pending_applications = OvertimeApplication.objects.filter(HR_approval="Pending", HOD_approval="Approved",
                                                              status="Pending")
    return pending_applications


def get_hod_in_department(approver):
    pass


def get_pending_overtime_applications(approver_user: User) -> dict:
    """Return a dictionary of pending applications per user role"""
    hod_pending_applications = OvertimeApplication.objects.none()
    hr_pending_applications = OvertimeApplication.objects.none()
    cfo_pending_applications = OvertimeApplication.objects.none()
    ceo_pending_applications = OvertimeApplication.objects.none()
    supervisor_pending_applications = OvertimeApplication.objects.none()
    is_supervisor = get_is_supervisor_in_team(approver_user)
    is_hod = get_is_hod_in_department(approver_user)

    if is_hod:
        hod_department = approver_user.solitonuser.employee.department
        hod_pending_applications = get_hod_pending_overtime_applications(hod_department)

    if approver_user.is_hr:
        hr_pending_applications = get_hr_pending_overtime_applications()

    if approver_user.is_cfo:
        cfo_pending_applications = get_cfo_pending_overtime_applications()

    if approver_user.is_ceo:
        ceo_pending_applications = get_ceo_pending_overtime_applications()

    if is_supervisor:
        supervisor = approver_user.solitonuser.employee
        supervisor_pending_applications = get_supervisor_pending_overtime_applications(supervisor)

    pending_applications = {
        "supervisor_pending_applications": supervisor_pending_applications,
        "hod_pending_applications": hod_pending_applications,
        "hr_pending_applications": hr_pending_applications,
        "cfo_pending_applications": cfo_pending_applications,
        "ceo_pending_applications": ceo_pending_applications,
    }
    return pending_applications


def get_recent_overtime_applications(limit, applicant):
    return OvertimeApplication.objects.filter(applicant=applicant).order_by('-id')[:limit]


def get_all_overtime_plans():
    overtime_plans = OvertimePlan.objects.all()
    return overtime_plans


def get_most_recent_overtime_plans():
    overtime_plans = OvertimePlan.objects.all().order_by('-id')
    return overtime_plans


def get_overtime_plan(overtime_plan_id):
    return OvertimePlan.objects.get(pk=overtime_plan_id)


def get_overtime_schedules(overtime_plan):
    return OvertimeSchedule.objects.filter(overtime_plan=overtime_plan).order_by('-id')


def get_hr_pending_overtime_plans():
    pending_overtime_plans = OvertimePlan.objects.filter(HR_approval="Pending",
                                                         status="Pending").order_by("-id")
    return pending_overtime_plans


def get_cfo_pending_overtime_plans():
    pending_overtime_plans = OvertimePlan.objects.filter(status="Pending", cfo_approval="Pending",
                                                         HR_approval="Approved").order_by("-id")
    return pending_overtime_plans


def get_pending_overtime_plans(approver):
    pending_overtime_plans = None

    if approver.is_hr:
        pending_overtime_plans = get_hr_pending_overtime_plans()

    if approver.is_cfo:
        pending_overtime_plans = get_cfo_pending_overtime_plans()

    return pending_overtime_plans


def get_supervisor_users(applicant):
    department = applicant.department
    all_supervisor_users = User.objects.filter(is_supervisor=True)
    users = []
    for supervisor_user in all_supervisor_users:
        if supervisor_user.solitonuser.employee.department == department:
            users.append(supervisor_user)

    return users


def get_supervisor_user(applicant):
    team = get_team_instance(applicant)
    supervisor = team.supervisor
    supervisor_user = supervisor.solitonuser.user
    return supervisor_user


def get_hod_users(applicant):
    department = applicant.department

    all_hod_users = User.objects.filter(is_hod=True)
    users = []
    for hod_user in all_hod_users:
        if hod_user.solitonuser.employee.department == department:
            users.append(hod_user)

    return users


def get_hr_users():
    all_hr_users = User.objects.filter(is_hr=True)
    return all_hr_users


def get_cfo_users():
    all_cfo_users = User.objects.filter(is_cfo=True)
    return all_cfo_users


def get_ceo_users():
    all_ceo_users = User.objects.filter(is_ceo=True)
    return all_ceo_users


def get_is_overtime_approver(approver_user: User) -> bool:
    is_supervisor = get_is_supervisor_in_team(approver_user)
    is_hod = get_is_hod_in_department(approver_user)
    return is_hod or approver_user.is_hr or approver_user.is_cfo or approver_user.is_ceo or is_supervisor


def get_approved_overtime_applications_in_current_month(applicant: Employee):
    """Pick applicant's overtime applications for the current month that are approved"""
    current_month = datetime.datetime.today().month
    overtime_applications = OvertimeApplication.objects.filter(date__month=current_month, applicant=applicant,
                                                               status="Approved")
    return overtime_applications
