from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_admin.decorators import log_activity
from ems_auth.decorators import training_full_auth_required, hr_required
from organisation_details.decorators import organisationdetail_required
from overtime.selectors import get_supervisor_users
from settings.selectors import get_all_currencies, get_currency
from training.models import Training, TrainingSchedule
from training.selectors import get_all_training_schedules, get_applicant_trainings, \
    get_training_schedule, get_pending_training_applications, get_training_application
from training.services import approve_training_application_service, reject_training_application_service, \
    send_training_application_mail


@organisationdetail_required
@log_activity
def user_training_page(request):
    applicant = request.user.solitonuser.employee
    if request.POST:
        programme = request.POST.get('programme')
        institution = request.POST.get('institution')
        duration = request.POST.get('duration')
        cost = request.POST.get('cost')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        business_case = request.POST.get('business_case')
        objectives = request.POST.get('objectives')
        preparations = request.POST.get('preparations')
        skills = request.POST.get('skills')
        knowledge = request.POST.get('knowledge')
        currency_id = request.POST.get('currency_id')
        currency = get_currency(currency_id)

        training_application = Training.objects.create(
            applicant=applicant,
            programme=programme,
            institution=institution,
            duration=duration,
            cost=cost,
            start_date=start_date,
            end_date=end_date,
            business_case=business_case,
            objectives=objectives,
            preparations=preparations,
            skills=skills,
            knowledge=knowledge,
            currency=currency
        )

        approvers = get_supervisor_users(applicant)

        send_training_application_mail(approvers, training_application)

        return HttpResponseRedirect(reverse(user_training_page))

    currencies = get_all_currencies()
    trainings = get_applicant_trainings(applicant)
    context = {
        "training_page": "active",
        "currencies": currencies,
        "trainings": trainings
    }

    return render(request, 'training/user_training.html', context)


@hr_required
@training_full_auth_required
@log_activity
def schedule_training_page(request):
    if request.POST:
        programme = request.POST.get('programme')
        duration = request.POST.get('duration')
        venue = request.POST.get('venue')
        purpose = request.POST.get('purpose')
        date = request.POST.get('date')

        TrainingSchedule.objects.create(
            programme=programme,
            duration=duration,
            venue=venue,
            purpose=purpose,
            date=date
        )

        return HttpResponseRedirect(reverse(schedule_training_page))

    training_schedules = get_all_training_schedules()
    context = {
        "training_page": "active",
        "training_schedules": training_schedules
    }

    return render(request, 'training/schedule_training.html', context)


@log_activity
def edit_training_schedule(request, training_schedule_id):
    if request.POST:
        programme = request.POST.get('programme')
        duration = request.POST.get('duration')
        venue = request.POST.get('venue')
        purpose = request.POST.get('purpose')
        date = request.POST.get('date')

        transaction_schedules = TrainingSchedule.objects.filter(id=training_schedule_id)
        transaction_schedules.update(
            programme=programme,
            duration=duration,
            venue=venue,
            purpose=purpose,
            date=date
        )

        return HttpResponseRedirect(reverse(schedule_training_page))

    training_schedule = get_training_schedule(training_schedule_id)
    context = {
        "training_page": "active",
        "training_schedule": training_schedule
    }
    return render(request, "training/edit_training_schedule.html", context)


@log_activity
def delete_training_schedule(request, training_schedule_id):
    training_schedule = get_training_schedule(training_schedule_id)
    training_schedule.delete()
    return HttpResponseRedirect(reverse(schedule_training_page))


@log_activity
def training_schedules_page(request):
    training_schedules = get_all_training_schedules()
    context = {
        "training_page": "active",
        "training_schedules": training_schedules
    }
    return render(request, 'training/training_schedules.html', context)


@organisationdetail_required
@log_activity
def approve_training_page(request):
    approver = request.user
    pending_applications = get_pending_training_applications(approver)
    context = {
        "training_page": "active",
        "pending_applications": pending_applications
    }
    return render(request, 'training/approve_training_applications.html', context)


@log_activity
def approve_training_application(request, training_application_id):
    approver = request.user
    training_application = get_training_application(training_application_id)
    approved_training_application = approve_training_application_service(approver, training_application)

    if approved_training_application:
        messages.success(request, "You approved %s's training application" % approved_training_application.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse('approve_training_page'))


@log_activity
def reject_training_application(request, training_application_id):
    rejecter = request.user
    training_application = get_training_application(training_application_id)
    rejected_training_application = reject_training_application_service(rejecter, training_application)
    if rejected_training_application:
        messages.success(request, "You rejected %s's training application" % rejected_training_application.applicant)
    else:
        messages.error(request, "You are not associated to any role on the system")
    return HttpResponseRedirect(reverse('approve_overtime_page'))


def pending_training_application_page(request, training_application_id):
    training_application = get_training_application(training_application_id)
    context = {
        "training_page": "active",
        "training_application": training_application
    }

    return render(request, 'training/pending_training_application.html', context)
