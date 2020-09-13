from django.contrib import messages
from django.shortcuts import render, redirect

from employees.selectors import get_active_employees, get_employee
from ems_admin.decorators import log_activity
from ems_auth.decorators import hr_required, ems_login_required, organisation_full_auth_required
from organisation_details.models import Position, Department, Team, SalaryScale
from organisation_details.selectors import get_all_departments, get_department, get_position, get_all_positions, get_all_teams, get_team, get_team_employees, get_department_employees, get_salary_scales, get_salary_scale
from ems_auth.decorators import hr_required, ems_login_required
from organisation_details.models import Position, Department, Team
from organisation_details.selectors import get_all_departments, get_department, get_position, get_all_positions, \
    get_all_teams, get_team, get_team_employees, get_department_employees
from settings.selectors import get_all_currencies, get_currency


@log_activity
def about_us(request):
    return render(request, "organisation_description.html")


@log_activity
def no_organisation_detail_page(request):
    context = {
        "organisation_detail_page": "active"
    }
    return render(request, 'no_organisation_detail.html', context)


@hr_required
@log_activity
def manage_teams_page(request):
    teams = get_all_teams()
    context = {
        "user": request.user,
        "organisation_page": "active",
        "teams": teams,
        "employees": get_active_employees(),
        "departments": get_all_departments()
    }

    return render(request, "organisation_details/manage_teams.html", context)


@log_activity
def add_new_team(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        supervisor_id = request.POST["supervisor_id"]
        department_id = request.POST["department_id"]

        supervisor = get_employee(supervisor_id)
        department = get_department(department_id)
        
        team = Team.objects.filter(name=team_name)

        if team:
            messages.warning(request, f'Team Already Exists')

            return redirect('manage_teams_page')
        else:
            team = Team(department=department, name=team_name, supervisor=supervisor)
            team.save()
            messages.success(request, f'Team {team_name} added Successfully Saved')

            return redirect('manage_teams_page')

    return redirect('manage_teams_page')


def edit_team_page(request, team_id):
    if request.POST:
        team = get_team(team_id)
        team_name = request.POST["team_name"]
        supervisor_id = request.POST["supervisor_id"]
        department_id = request.POST["department_id"]
        supervisor = get_employee(supervisor_id)
        department = get_department(department_id)
        team.department = department
        team.supervisor = supervisor
        team.name = team_name
        team.save()

        messages.success(request, f'Team Info changed Successfully')
        return redirect('manage_teams_page')

    context = {
        "user": request.user,
        "team":  get_team(team_id),
        "employees": get_active_employees(),
        "departments": get_all_departments(),
        "organisation_page": "active"
    }
    return render(request, 'organisation_details/edit_team.html', context)


def delete_team(request, team_id):
    try:
        team = get_team(team_id)
        team.delete()
        messages.success(request, f'Team Deleted Successfully')
        return redirect('manage_teams_page')
    except Team.DoesNotExist:
        messages.error(request, f'The team no longer exists on the system')

    return redirect('manage_teams_page')


# Department Section
@hr_required
@log_activity
def manage_departments_page(request):
    context = {
        "user": request.user,
        "organisation_page": "active",
        "departments": get_all_departments(),
        "employees": get_active_employees(),
    }

    return render(request, "organisation_details/manage_departments.html", context)


@log_activity
def add_new_department(request):
    if request.method == "POST":
        department_name = request.POST["department_name"]
        employee_id = request.POST["employee_id"]
        employee = get_employee(employee_id)

        department = Department.objects.filter(name=department_name)

        if department:
            messages.warning(request, f'Department {department_name} Already Exists')

            return redirect('manage_departments_page')
        else:
            department = Department(name=department_name, hod=employee)
            department.save()
            messages.success(request, f'Department {department_name} Successfully Saved')
            return redirect('manage_departments_page')

    return redirect('manage_departments_page')


def edit_department(request):
    if request.method == "POST":
        department_id = request.POST.get('department_id')
        employee_id = request.POST.get('employee_id')
        employee = get_employee(employee_id)
        department = get_department(department_id)
        department.name = request.POST.get('department_name')
        department.hod = employee
        department.save()

        messages.success(request, f'Department Info Changed Successfully')
        return redirect('manage_departments_page')

    messages.error(request, f'Changes Not Saved, Check your inputs and try again!')
    return redirect('manage_departments_page')


@log_activity
def edit_department_page(request, department_id):
    department = get_department(department_id)
    context = {
        "user": request.user,
        "employees": get_active_employees(),
        "department": department,
        "organisation_page": "active"
    }
    return render(request, 'organisation_details/edit_department.html', context)


@log_activity
def delete_department(request, department_id):
    try:
        department = get_department(department_id)
        department.delete()
        messages.success(request, f'Department Deleted Successfully')
        return redirect('manage_departments_page')
    except Department.DoesNotExist:
        messages.error(request, f'The department no longer exists on the system')

    return redirect('manage_departments_page')


@ems_login_required
@hr_required
@log_activity
def manage_job_positions_page(request):
    context = {
        "user": request.user,
        "organisation_page": "active",
        "positions": get_all_positions(),
        "currencies": get_all_currencies(),
        "scales": get_salary_scales(),
    }

    return render(request, "organisation_details/manage_job_positions.html", context)


# Job Titles'
@log_activity
def add_new_job_position(request):
    if request.method == "POST":
        job_title = request.POST["job_title"]
        pos = request.POST["positions"]
        type = request.POST.get('type')
        salary = get_salary_scale(request.POST.get('salary'))
        currency_id = request.POST.get('currency')
        description = request.POST.get('description')

        currency = get_currency(currency_id)

        job = Position.objects.filter(name=job_title)

        if job:
            messages.warning(request, f'Position {job_title} Already Exists')

            return redirect('manage_job_positions_page')
        else:
            job = Position(name=job_title, number_of_slots=pos, type=type, salary_scale=salary,
                        currency=currency, description=description)
            job.save()

            messages.success(request, f'Position {job_title} added Successfully')
            return redirect('manage_job_positions_page')

        messages.error(request, f'Information Not Saved, Check you inputs and try again!')

    return redirect('manage_job_positions_page')


def edit_job_position_page(request, position_id):
    position = get_position(position_id)
    context = {
        "user": request.user,
        "position": position,
        "scales": get_salary_scales(),
        "currencies": get_all_currencies(),
        "organisation_page": "active"

    }
    return render(request, 'organisation_details/edit_position.html', context)


@log_activity
def edit_job_position(request):
    if not request.POST:
        return redirect('manage_job_positions_page')

    position_id = request.POST.get('position_id')
    currency_id = request.POST.get('currency')
    currency = get_currency(currency_id)
    position = get_position(position_id)
    position.name = request.POST.get('name')
    position.number_of_slots = request.POST.get('number_of_slots')
    position.type = request.POST.get('type')
    position.salary_scale = get_salary_scale(request.POST.get('salary'))
    position.currency = currency
    position.description = request.POST.get('description')
    position.save()
    messages.success(request, "Changes successfully Saved")
    return redirect('manage_job_positions_page')


@log_activity
def delete_job_position(request, position_id):
    try:
        position = get_position(position_id)
        position.delete()
        messages.success(request, f'Job Position Deleted Successfully')
        return redirect('manage_job_positions_page')
    except Position.DoesNotExist:
        messages.error(request, f'The Job Position no longer exists on the system')

    return redirect('manage_job_positions_page')

@log_activity
def team_employees(request, team_id):
    team_employees=get_team_employees(team_id)

    team = get_team(team_id)
    context={
        "employees": team_employees,
        "team": team
    }

    return render(request, "organisation_details/team_employees.html", context)

@log_activity
def department_employees(request, department_id):
    department_employees=get_department_employees(department_id)

    department = get_department(department_id)
    context={
        "employees": department_employees,
        "department": department
    }

    return render(request, "organisation_details/department_employees.html", context)

@log_activity
def manage_salary_scale_page(request):
    context = {
        "organisation_page": "active",
        "user": request.user,
        "scales": get_salary_scales(),
    }

    return render(request, "organisation_details/manage_salary_scale.html", context)

@log_activity
def add_new_salary_scale(request):
    if request.method=="POST":
        scale_level = request.POST.get('scale_level')
        minimum = request.POST.get('min_value')
        maximum = request.POST.get('max_value')

        salary_scale = SalaryScale.objects.filter(level=scale_level)

        if salary_scale:
            messages.warning(request, f'Salary Scale {salary_scale} Already Exists')

            return redirect('manage_salary_scale_page')
        else:
            salary_scale = SalaryScale(level=scale_level, minimum=minimum, maximum=maximum)

            salary_scale.save()

            messages.success(request, f'Salary Scale {salary_scale} Saved Successfully!')

            return redirect('manage_salary_scale_page')

        messages.error(request, f'Information Not Saved, Check you inputs and try again!')

    return redirect('manage_salary_scale_page')

@log_activity
def edit_salary_scale_page(request, scale_id):
    scale = get_salary_scale(scale_id)
    context = {
        "user": request.user,
        "scale": scale,
        "organisation_page": "active"

    }
    return render(request, 'organisation_details/edit_salary_scale.html', context)

@log_activity
def edit_salary_scale(request):
    if request.method=="POST":
        scale_id = request.POST.get('scale_id')
        salary_scale = get_salary_scale(scale_id)

        salary_scale.level=request.POST.get('grade_level')
        salary_scale.minimum=request.POST.get('min_value')
        salary_scale.maximum = request.POST.get('max_value')

        salary_scale.save()

        messages.success(request, f'Changes Saved Successfully!')

        return redirect('manage_salary_scale_page')

@log_activity
def delete_salary_scale(request, scale_id):
    try:
        salary_scale=get_salary_scale(scale_id)

        salary_scale.delete()
        return redirect('manage_salary_scale_page')
    except SalaryScale.DoesNotExist:
        messages.warning(request, f"Salary Grade Doesn't Exist")
        
        return redirect('manage_salary_scale_page')