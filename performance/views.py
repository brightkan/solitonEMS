# Create your views here.

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from employees.selectors import get_employee, get_active_employees
from ems_admin.decorators import log_activity
from ems_auth.decorators import hod_required
from organisation_details.decorators import organisationdetail_required
from organisation_details.models import OrganisationDetail
from performance.models import DepartmentKPI, EmployeeKPI
from performance.procedures import calculate_performance_rating
from performance.selectors import get_all_department_kpi, get_department_kpi, get_all_employee_kpi, get_employee_kpi
from django.shortcuts import render


@hod_required
def manage_department_kpi(request):
    employee = request.user.solitonuser.employee
    department = employee.organisationdetail.department
    department_kpis = get_all_department_kpi(department)

    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")
        try:
            if score > weight:
                messages.warning(request, "Department KPI added successfully")
                return HttpResponseRedirect(reverse(manage_department_kpi))
            DepartmentKPI.objects.create(
                measure_of_success=measure_of_success,
                weight=weight,
                score=score,
                department=department,
            )
            messages.warning(request, "Department KPI added successfully")
            return HttpResponseRedirect(reverse(manage_department_kpi))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add performance KPI")

    context = {
        "performance_page": "active",
        "department_kpis": department_kpis,
    }
    return render(request, "performance/manage_department_kpi.html", context)


@hod_required
@log_activity
def edit_performance_kpi_page(request, kpi_id):
    department_kpi = get_department_kpi(kpi_id)

    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")
        department_kpi_list = DepartmentKPI.objects.filter(id=kpi_id)
        try:
            department_kpi_list.update(
                measure_of_success=measure_of_success,
                weight=weight,
                score=score,
            )
            return HttpResponseRedirect(reverse(manage_department_kpi))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to edit performance KPI")

    context = {
        "performance_page": "active",
        "department_kpi": department_kpi

    }
    return render(request, 'performance/edit_department_kpi.html', context)


@hod_required
def delete_performance_kpi(request, kpi_id):
    department_kpi = get_department_kpi(kpi_id)
    department_kpi.delete()
    return HttpResponseRedirect(reverse(manage_department_kpi))


@hod_required
def manage_employees_kpi(request):
    employee = request.user.solitonuser.employee
    department = employee.organisationdetail.department
    organisationdetails = OrganisationDetail.objects.filter()
    context = {
        "performance_page": "active",
        "organisationdetails": organisationdetails,
    }
    return render(request, "performance/manage_employees_kpi.html", context)


@hod_required
def manage_employee_kpi(request, employee_id):
    employee = get_employee(employee_id)
    employee_kpis = get_all_employee_kpi(employee=employee)
    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")

        if score > weight:
            messages.warning(request, "Employee KPI added successfully")
            return HttpResponseRedirect(reverse(manage_department_kpi))

        try:
            EmployeeKPI.objects.create(
                measure_of_success=measure_of_success,
                weight=weight,
                score=score,
                employee=employee,
            )
            messages.warning(request, "Employee KPI added successfully")
            return HttpResponseRedirect(reverse(manage_employee_kpi, args=[employee.id]))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add performance KPI")
    context = {
        "performance_page": "active",
        "employee_kpis": employee_kpis,
        "employee": employee,
    }
    return render(request, "performance/manage_employee_kpi.html", context)


@hod_required
@log_activity
def edit_employee_kpi_page(request, kpi_id):
    employee_kpi = get_employee_kpi(kpi_id)
    employee = employee_kpi.employee
    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")
        employee_kpi_list = EmployeeKPI.objects.filter(id=kpi_id)
        try:
            employee_kpi_list.update(
                measure_of_success=measure_of_success,
                weight=weight,
                score=score,
            )
            messages.warning(request, "Employee KPI updated")
            return HttpResponseRedirect(reverse(manage_employee_kpi, args=[employee.id]))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to edit performance KPI")

    context = {
        "performance_page": "active",
        "employee_kpi": employee_kpi

    }
    return render(request, 'performance/edit_employee_kpi.html', context)


@hod_required
def delete_employee_kpi(request, kpi_id):
    employee_kpi = get_employee_kpi(kpi_id)
    employee = employee_kpi.employee
    employee_kpi.delete()
    messages.warning(request, "Employee KPI deleted")
    return HttpResponseRedirect(reverse(manage_employee_kpi, args=[employee.id]))


@hod_required
@organisationdetail_required
def manage_your_kpi(request):
    employee = request.user.solitonuser.employee
    employee_kpis = get_all_employee_kpi(employee=employee)

    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")

        if score > weight:
            messages.warning(request, "Employee KPI added successfully")
            return HttpResponseRedirect(reverse(manage_department_kpi))
        try:
            EmployeeKPI.objects.create(
                measure_of_success=measure_of_success,
                weight=weight,
                score=score,
                employee=employee,
                assessor="Self"
            )
            messages.warning(request, "Your KPI added successfully")
            return HttpResponseRedirect(reverse(manage_your_kpi))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add performance KPI")
    context = {
        "performance_page": "active",
        "employee_kpis": employee_kpis,
        "employee": employee,
    }
    return render(request, "performance/manage_your_kpi.html", context)


def edit_your_kpi_page(request, kpi_id):
    employee_kpi = get_employee_kpi(kpi_id)
    if request.POST:
        measure_of_success = request.POST.get("measure_of_success")
        weight = request.POST.get("weight")
        score = request.POST.get("score")
        employee_kpi_list = EmployeeKPI.objects.filter(id=kpi_id)

        employee_kpi_list.update(
            measure_of_success=measure_of_success,
            weight=weight,
            score=score,
        )
        try:

            messages.warning(request, "Your KPI updated")
            return HttpResponseRedirect(reverse(manage_your_kpi))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to edit performance KPI")

    context = {
        "performance_page": "active",
        "employee_kpi": employee_kpi

    }
    return render(request, 'performance/edit_your_kpi.html', context)


def delete_your_kpi(request, kpi_id):
    employee_kpi = get_employee_kpi(kpi_id)
    employee_kpi.delete()
    messages.warning(request, "Your KPI has been deleted")
    return HttpResponseRedirect(reverse(manage_your_kpi))


@hod_required
def employees_performance_ratings_page(request):
    employees = get_active_employees()
    context = {
        "performance_page": "active",
        "employees": employees,
    }
    return render(request, "performance/employees_performance_rating.html", context)


def employee_performance_ratings_page(request):
    employee = request.user.solitonuser.employee
    department = employee.organisationdetail.department
    department_kpis = get_all_department_kpi(department)
    employee_kpis = get_all_employee_kpi(employee=employee)
    performance_rating = calculate_performance_rating(employee)

    context = {
        "performance_page": "active",
        "employee": employee,
        "employee_kpis": employee_kpis,
        "department_kpis": department_kpis,
        "performance_rating": performance_rating
    }
    return render(request, "performance/employee_performance_ratings.html", context)
