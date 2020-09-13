from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from employees.selectors import get_active_employees, get_employee
from ems_admin.decorators import log_activity
from ems_auth.decorators import ems_login_required, hod_required, hr_required
from notification.services import create_notification
from organisation_details.decorators import organisationdetail_required

from overtime.models import OvertimeApplication, OvertimePlan, OvertimeSchedule
from overtime.procedures import is_duration_valid
from overtime.selectors import get_all_overtime_applications, get_pending_overtime_applications, \
    get_overtime_application, get_recent_overtime_applications, get_most_recent_overtime_plans, \
    get_overtime_plan, get_overtime_schedules, get_pending_overtime_plans, get_supervisor_user
from overtime.services import reject_overtime_application_service, approve_overtime_application_service, \
    update_overtime_application, reject_overtime_plan_service, approve_overtime_plan_service, \
    send_overtime_application_mail


# Create your views here.
@ems_login_required
@organisationdetail_required
@log_activity
def approve_overtime_page(request):
    approver_user = request.user
    pending_applications = get_pending_overtime_applications(approver_user)
    context = {
        "overtime_page": "active",
        "supervisor_pending_applications": pending_applications["supervisor_pending_applications"],
        "hod_pending_applications": pending_applications["hod_pending_applications"],
        "hr_pending_applications": pending_applications["hr_pending_applications"],
        "cfo_pending_applications": pending_applications["cfo_pending_applications"],
        "ceo_pending_applications": pending_applications["ceo_pending_applications"],

    }
    return render(request, 'overtime/overtime_page.html', context)


@ems_login_required
@organisationdetail_required
@log_activity
def apply_for_overtime_page(request):
    applicant = request.user.solitonuser.employee
    if request.POST:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')
        if not is_duration_valid(start_time, end_time):
            messages.error(request, "Duration for the overtime application is not valid")
            return HttpResponseRedirect(reverse("apply_for_overtime_page"))

        overtime_application = OvertimeApplication.objects.create(
            start_time=start_time,
            end_time=end_time,
            description=description,
            applicant=applicant
        )
        approver = get_supervisor_user(applicant)
        message = "You need to approve/reject overtime application from {}".format(applicant)
        create_notification("Overtime", message, [approver])
        approver = get_supervisor_user(applicant)
        # send_overtime_application_mail([approver], overtime_application)
        messages.success(request, "You have successfully submitted your overtime application")
        return HttpResponseRedirect(reverse('apply_for_overtime_page'))

    recent_applications = get_recent_overtime_applications(limit=5, applicant=applicant)
    context = {
        "overtime_page": "active",
        "recent_applications": recent_applications
    }
    return render(request, 'overtime/apply_for_overtime.html', context)


@hr_required
@ems_login_required
@log_activity
def overtime_applications_page(request):
    context = {
        "overtime_page": "active",
        "overtime_applications": get_all_overtime_applications()
    }

    return render(request, 'overtime/overtime_applications.html', context)


@ems_login_required
@log_activity
def approved_overtime_applications_page(request):
    # Get the approved overtime applications
    approved_applications = OvertimeApplication.objects.filter(status="Approved")
    context = {
        "overtime_page": "active",
        "approved_applications": approved_applications
    }
    return render(request, 'overtime/approved_applications_page.html', context)


@log_activity
def amend_overtime_application_page(request, overtime_application_id):
    overtime_application = get_overtime_application(overtime_application_id)
    if request.POST:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')
        update_overtime_application(overtime_application.id, start_time, end_time, description)
        messages.success(request, "Successfully amended the overtime application")
        return HttpResponseRedirect(reverse('approve_overtime_page'))

    context = {
        "overtime_page": "active",
        "overtime_application": overtime_application
    }

    return render(request, 'overtime/amend_overtime_application.html', context)


@log_activity
def pending_overtime_application_page(request, overtime_application_id):
    overtime_application = get_overtime_application(overtime_application_id)

    context = {
        "overtime_page": "active",
        "overtime_application": overtime_application
    }

    return render(request, 'overtime/pending_overtime_application.html', context)


def reject_overtime_application(request, overtime_application_id):
    rejecter = request.user
    overtime_application = get_overtime_application(overtime_application_id)
    rejected_overtime_application = reject_overtime_application_service(rejecter, overtime_application)
    if rejected_overtime_application:
        messages.success(request, "You rejected %s's overtime application" % rejected_overtime_application.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse('approve_overtime_page'))


def approve_overtime_application(request, overtime_application_id):
    approver = request.user
    overtime_application = get_overtime_application(overtime_application_id)
    approved_overtime_application = approve_overtime_application_service(approver, overtime_application)
    if approved_overtime_application:
        messages.success(request, "You approved %s's overtime application" % approved_overtime_application.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse('approve_overtime_page'))


@hod_required
def create_overtime_plan_page(request):
    context = {
        "overtime_plans": get_most_recent_overtime_plans()
    }
    return render(request, 'overtime/create_overtime_plan.html', context)


def create_overtime_plan(request):
    hod = request.user.solitonuser.employee
    overtime_plan = OvertimePlan.objects.create(
        applicant=hod
    )
    return HttpResponseRedirect(reverse(create_overtime_plan_page))


@hod_required
def add_overtime_schedule_page(request, overtime_plan_id):
    overtime_plan = get_overtime_plan(overtime_plan_id)
    if request.POST:
        employee_id = request.POST["employee"]
        employee = get_employee(employee_id)
        date = request.POST["date"]
        number_of_hours = request.POST["number_of_hours"]
        description = request.POST["description"]

        OvertimeSchedule.objects.create(
            employee=employee,
            overtime_plan=overtime_plan,
            date=date,
            number_of_hours=number_of_hours,
            description=description,
        )
        return HttpResponseRedirect(reverse(add_overtime_schedule_page, args=[overtime_plan.id]))

    context = {
        "employees": get_active_employees(),
        "overtime_schedules": get_overtime_schedules(overtime_plan)
    }
    return render(request, 'overtime/add_employee_schedules.html', context)


def approve_overtime_plans_page(request):
    approver = request.user
    pending_overtime_plans = get_pending_overtime_plans(approver)
    context = {
        "overtime_page": "active",
        "pending_overtime_plans": pending_overtime_plans
    }
    return render(request, 'overtime/approve_overtime_plans.html', context)


def pending_overtime_plan_page(request, overtime_plan_id):
    overtime_plan = get_overtime_plan(overtime_plan_id)
    overtime_schedules = get_overtime_schedules(overtime_plan)
    context = {
        "overtime_page": "active",
        "overtime_plan": overtime_plan,
        "overtime_schedules": overtime_schedules
    }

    return render(request, 'overtime/pending_overtime_plan.html', context)


@log_activity
def reject_overtime_plan(request, overtime_plan_id):
    rejecter = request.user
    overtime_plan = get_overtime_plan(overtime_plan_id)
    rejected_overtime_plan = reject_overtime_plan_service(rejecter, overtime_plan)
    if rejected_overtime_plan:
        messages.success(request, "You rejected %s's overtime plan" % rejected_overtime_plan.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse(approve_overtime_plans_page))


@log_activity
def approve_overtime_plan(request, overtime_plan_id):
    approver = request.user
    overtime_plan = get_overtime_plan(overtime_plan_id)
    approved_overtime_plan = approve_overtime_plan_service(approver, overtime_plan)
    if approved_overtime_plan:
        messages.success(request, "You approved %s's overtime plan" % approved_overtime_plan.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse(approve_overtime_plans_page))


def delete_overtime_application(request,id):
    """Delete overtime application"""
    overtime_application = get_overtime_application(id)
    overtime_application.delete()
    return HttpResponseRedirect(reverse(overtime_applications_page))