from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_admin.decorators import log_activity
from ems_auth.decorators import hr_required
from organisation_details.selectors import get_all_positions, get_position
from recruitment.forms import JobApplicationForm
from recruitment.models import JobAdvertisement
from recruitment.selectors import get_all_job_ads, get_job_advertisement, get_job_applications


@hr_required
@log_activity
def manage_job_advertisement_page(request):
    if request.POST:
        position_id = request.POST.get('position_id')
        position = get_position(position_id)

        education = request.POST.get('education')
        vacancy = request.POST.get('vacancy')
        experience = request.POST.get('experience')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        JobAdvertisement.objects.create(
            position=position,
            education=education,
            vacancy=vacancy,
            experience=experience,
            description=description,
            deadline=deadline
        )

        messages.success(request, "Successfully created a job advertisement")

        return HttpResponseRedirect(reverse('manage_job_advertisement_page'))

    all_positions = get_all_positions()
    all_job_ads = get_all_job_ads()
    context = {
        "recruitment_page": "active",
        "positions": all_positions,
        "job_ads": all_job_ads,

    }
    return render(request, 'recruitment/manage_job_advertisement.html', context)


@log_activity
def edit_job_advertisement_page(request, job_advertisement_id):
    if request.POST:
        position_id = request.POST.get('position_id')
        position = get_position(position_id)

        education = request.POST.get('education')
        vacancy = request.POST.get('vacancy')
        experience = request.POST.get('experience')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        JobAdvertisement.objects.filter(id=job_advertisement_id).update(
            position=position,
            education=education,
            vacancy=vacancy,
            experience=experience,
            description=description,
            deadline=deadline
        )

        messages.success(request, "Successfully updated a job advertisement")
        return HttpResponseRedirect(reverse('manage_job_advertisement_page'))

    job_advertisement = get_job_advertisement(job_advertisement_id)
    all_positions = get_all_positions()
    all_job_ads = get_all_job_ads()
    context = {
        "recruitment_page": "active",
        "positions": all_positions,
        "job_ads": all_job_ads,
        "job_ad": job_advertisement,
    }
    return render(request, 'recruitment/edit_job_advertisement.html', context)


@log_activity
def delete_job_advertisement(request, job_advertisement_id):
    job_advertisement = get_job_advertisement(job_advertisement_id)
    job_advertisement.delete()
    messages.success(request, "Deleted the job advertisement")
    return HttpResponseRedirect(reverse('manage_job_advertisement_page'))


@log_activity
def job_advertisements_page(request):
    all_positions = get_all_positions()
    all_job_ads = get_all_job_ads()

    context = {
        "recruitment_page": "active",
        "positions": all_positions,
        "job_ads": all_job_ads,

    }

    return render(request, 'recruitment/advertised_jobs.html', context)


@hr_required
@log_activity
def view_job_applications_page(request):
    all_positions = get_all_positions()
    all_job_ads = get_all_job_ads()

    context = {
        "recruitment_page": "active",
        "positions": all_positions,
        "job_ads": all_job_ads,

    }

    return render(request, 'recruitment/view_job_applications.html', context)


@log_activity
def job_advertisement(request, job_advertisement_id):
    if request.POST:
        job_application_form = JobApplicationForm(request.POST, request.FILES)
        job_application = job_application_form.save(commit=False)
        job_application.applicant = request.user.solitonuser.employee
        job_application.job_ad = get_job_advertisement(job_advertisement_id)
        job_application.save()

        messages.success(request, "Successfully uploaded CV")
        return HttpResponseRedirect(reverse('job_advertisement', args=[job_advertisement_id]))

    job_advertisement = get_job_advertisement(job_advertisement_id)

    job_application_form = JobApplicationForm()
    context = {
        "recruitment_page": "active",
        "job_advertisement": job_advertisement,
        "job_application_form": job_application_form,

    }

    return render(request, 'recruitment/job_description.html', context)


@log_activity
def job_applications_page(request, job_advertisement_id):
    job_advertisement = get_job_advertisement(job_advertisement_id)
    job_applications = get_job_applications(job_advertisement)

    context = {
        "recruitment_page": "active",
        "job_applications": job_applications,
        "job_advertisement": job_advertisement
    }
    return render(request, 'recruitment/job_applications.html', context)
