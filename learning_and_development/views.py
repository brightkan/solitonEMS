from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_admin.decorators import log_activity
from ems_auth.decorators import hr_required
from learning_and_development.models import Resource
from learning_and_development.selectors import get_all_resources, get_resource
from organisation_details.selectors import get_all_departments, get_department


@hr_required
@log_activity
def manage_resources_page(request):
    if request.POST and request.FILES:
        name = request.POST.get('name')
        year_published = request.POST.get('year_published')
        producer = request.POST.get('producer')
        file_format = request.POST.get('file_format')
        department_id = request.POST.get('department')
        department = get_department(department_id)
        description = request.POST.get('description')
        file = request.FILES.get('file')

        Resource.objects.create(
            name=name,
            year_published=year_published,
            producer=producer,
            file_format=file_format,
            department=department,
            description=description,
            file=file,
        )

        return HttpResponseRedirect(reverse(manage_resources_page))

    resources = get_all_resources()
    departments = get_all_departments()
    context = {
        "learning_and_development_page": "active",
        "departments": departments,
        "resources": resources,
    }

    return render(request, 'learning_and_development/manage_resources.html', context)


@log_activity
def edit_resource_page(request, resource_id):
    resource = get_resource(resource_id)
    if request.POST:
        name = request.POST.get('name')
        year_published = request.POST.get('year_published')
        producer = request.POST.get('producer')
        file_format = request.POST.get('file_format')
        department_id = request.POST.get('department')
        department = get_department(department_id)
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if not file:
            file = resource.file

        Resource.objects.filter(id=resource_id).update(
            name=name,
            year_published=year_published,
            producer=producer,
            file_format=file_format,
            department=department,
            description=description,
            file=file,
        )

        return HttpResponseRedirect(reverse(manage_resources_page))

    departments = get_all_departments()
    context = {
        "learning_and_development_page": "active",
        "resource": resource,
        "departments": departments
    }
    return render(request, 'learning_and_development/edit_resource.html', context)


@log_activity
def delete_resource(request, resource_id):
    resource = get_resource(resource_id)
    resource.delete()
    return HttpResponseRedirect(reverse(manage_resources_page))


@log_activity
def resources_page(request):
    if request.POST:
        department_id = request.POST.get('department_id')
        if department_id:
            try:
                department = get_department(department_id)
            except ValueError:
                return HttpResponseRedirect(reverse(resources_page))

            department = get_department(department_id)
            departments = get_all_departments()
            departments = get_all_departments()
            resources = get_all_resources()
            context = {
                "learning_and_development_page": "active",
                "departments": departments,
                "resources": Resource.objects.filter(department=department)
            }
            return render(request, 'learning_and_development/resources.html', context)
        else:
            return HttpResponseRedirect(reverse(resources_page))

    departments = get_all_departments()
    resources = get_all_resources()
    context = {
        "learning_and_development_page": "active",
        "departments": departments,
        "resources": resources
    }
    return render(request, 'learning_and_development/resources.html', context)


@log_activity
def books_page(request):
    if request.POST:
        department_id = request.POST.get('department_id')
        if department_id:
            try:
                department = get_department(department_id)
            except ValueError:
                return HttpResponseRedirect(reverse(books_page))

            department = get_department(department_id)
            departments = get_all_departments()
            departments = get_all_departments()
            resources = get_all_resources()
            context = {
                "learning_and_development_page": "active",
                "departments": departments,
                "resources": Resource.objects.filter(department=department, file_format="book")
            }
            return render(request, 'learning_and_development/books.html', context)
        else:
            return HttpResponseRedirect(reverse(books_page))

    books = Resource.objects.filter(file_format='book')
    departments = get_all_departments()
    context = {
        "learning_and_development_page": "active",
        "departments": departments,
        "resources": books

    }
    return render(request, 'learning_and_development/books.html', context)


@log_activity
def videos_page(request):
    if request.POST:
        department_id = request.POST.get('department_id')
        if department_id:
            try:
                department = get_department(department_id)
            except ValueError:
                return HttpResponseRedirect(reverse(videos_page))

            department = get_department(department_id)
            departments = get_all_departments()
            departments = get_all_departments()
            resources = get_all_resources()
            context = {
                "learning_and_development_page": "active",
                "departments": departments,
                "resources": Resource.objects.filter(department=department, file_format="video")
            }
            return render(request, 'learning_and_development/videos.html', context)
        else:
            return HttpResponseRedirect(reverse(videos_page))

    videos = Resource.objects.filter(file_format='video')
    departments = get_all_departments()
    context = {
        "learning_and_development_page": "active",
        "departments": departments,
        "resources": videos

    }
    return render(request, 'learning_and_development/videos.html', context)


@log_activity
def audios_page(request):
    if request.POST:
        department_id = request.POST.get('department_id')
        if department_id:
            try:
                department = get_department(department_id)
            except ValueError:
                return HttpResponseRedirect(reverse(videos_page))

            department = get_department(department_id)
            departments = get_all_departments()
            departments = get_all_departments()
            resources = get_all_resources()
            context = {
                "learning_and_development_page": "active",
                "departments": departments,
                "resources": Resource.objects.filter(department=department, file_format='audio')
            }
            return render(request, 'learning_and_development/audios.html', context)
        else:
            return HttpResponseRedirect(reverse(videos_page))

    audios = Resource.objects.filter(file_format='audio')
    departments = get_all_departments()
    context = {
        "learning_and_development_page": "active",
        "departments": departments,
        "resources": audios

    }
    return render(request, 'learning_and_development/audios.html', context)
