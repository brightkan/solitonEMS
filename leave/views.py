from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.utils import timezone
import datetime
from datetime import timedelta
from datetime import date
import calendar
from calendar import HTMLCalendar
from collections import namedtuple
from employees.models import Employee, Department, Team
from django.db import connection
from django.db.models import (
    Sum,
    Count
)
from .models import (
    Leave_Types,
    Holidays,
    LeaveApplication,
    annual_planner,
    Leave_Records
)


def get_current_user(request, need):
    user = request.user  # getting the current logged in User

    cur_user = f'{user.solitonuser.employee.first_name} {user.solitonuser.employee.last_name}'
    # cur_role = user.solitonuser.soliton_role.name
    user_department = user.solitonuser.employee.organisationdetail.department.id
    user_team = user.solitonuser.employee.organisationdetail.team.id
    cur_id = user.solitonuser.employee.id
    gender = user.solitonuser.employee.gender

    if need == "name":
        return cur_user
    elif need == "dept":
        return user_department
    elif need == "team":
        return user_team
    elif need == "id":
        return cur_id
    elif need == "gender":
        return gender
    else:
        return 0


@login_required
def leave_dashboard_page(request):
    applications = ""
    user = request.user
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'ems_auth/login.html', {"message": None})

    user_role = get_current_user(request, "role")

    is_team_supervisor = Team.objects.filter(id=get_current_user(request, "team"), \
                                             supervisors=get_current_user(request, "id")).count()

    is_hod = Department.objects.filter(id=get_current_user(request, "dept"), \
                                       hod=get_current_user(request, "id")).count()

    is_hod = Department.objects.filter(id=get_current_user(request,"dept"),\
         hod=get_current_user(request,"id")).count()

    print("is Supervisor: ", is_team_supervisor)

    if is_team_supervisor == 1:
        print("As Supervisor")
        print("Team: ", get_current_user(request,"team"))
        print("ID: ", get_current_user(request,"id"))
        applications = LeaveApplication.objects.filter(supervisor_status="Pending",\
             team=get_current_user(request,"team")).order_by('apply_date')
        print("Apps: ", applications)
    
    elif is_hod == 1:
        print("As HOD")
        applications = LeaveApplication.objects.filter(hod_status="Pending", \
            supervisor_status="Approved", department=get_current_user(request, "team")) \
            .order_by('apply_date')

    if user.is_hr:
        print("As Hr")
        applications = LeaveApplication.objects \
            .filter(hr_status="Pending", supervisor_status="Approved", \
                    hod_status="Approved").order_by('apply_date')
    else:
        applications = ""

    leave_types = Leave_Types.objects.all()

    leave_types_dict = {}
    for typ in leave_types:
        leave_count = LeaveApplication.objects.filter(leave_type=typ).count()
        leave_types_dict.update({typ: leave_count})

    context = {
        "leave_dashboard_page": "active",
        "applications": applications,
        "maternity": LeaveApplication.objects.filter(leave_type=1).count(),
        "paternity": LeaveApplication.objects.filter(leave_type=2).count(),
        "compassionate": LeaveApplication.objects.filter(leave_type=3).count(),
        "annual": LeaveApplication.objects.filter(leave_type=4).count(),
        # "sick": LeaveApplication.objects.filter(leave_type=5).count(),
    }
    return render(request, 'leave/dashboard.html', context)


def leave_types_page(request):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'ems_auth/login.html', {"message": None})

    context = {
        "leave_page": "active",
        "types": Leave_Types.objects.all()
    }
    return render(request, 'leave/leave_types.html', context)


def add_new_type(request):
    if request.method == 'POST':
        # Fetching data from the add new leave type form
        leave_type = request.POST['leave_type']
        leave_days = request.POST['leave_days']
        desc = request.POST['desc']

        try:
            # Creating instance of Leave Types
            type_leave = Leave_Types(leave_type=leave_type, leave_days=leave_days, description=desc)

            # Saving the leave type instance
            type_leave.save()
            messages.success(request, f'Info Successfully Saved')

            return redirect('leave_types_page')

        except:
            messages.error(request, f'Info Not Saved, Check Your inputs and try again!!!')

            return redirect('leave_types_page')

    else:
        context = {
            "leave_types_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
def edit_leave_type_page(request, id):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'ems_auth/login.html', {"message": None})

    leave = Leave_Types.objects.get(pk=id)

    context = {
        "leave_page": "active",
        "leave": leave
    }
    return render(request, 'leave/leave_type.html', context)


def holidays_page(request):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'ems_auth/login.html', {"message": None})

    context = {
        "leave_page": "active",
        "holidays": Holidays.objects.all()
    }
    return render(request, 'leave/holidays.html', context)


def add_new_holiday(request):
    if request.method == 'POST':
        # Fetching data from the add new holiday form
        hol_name = request.POST['hol_name']
        hol_date = request.POST['hol_date']
        duration = request.POST['duration']

        try:

            hols = Holidays(holiday_date=hol_date, holiday_name=hol_name, duration=duration)
            hols.save()

            messages.success(request, f'Info Successfully Saved')
            return redirect('holidays_page')

        except:
            messages.error(request, f'Infor Not Saved, Check you inputs and try again!')

            return redirect('holidays_page')


def apply_leave_page(request):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'ems_auth/login.html', {"message": None})

    employee = Employee.objects.filter(pk=get_current_user(request, "id"))
    leave_record = Leave_Records.objects.all()
    employee_record = leave_record.get(employee=get_current_user(request, "id"), leave_year=date.today().year)

    context = {
        "leave_page": "active",
        "apps": LeaveApplication.objects.filter(employee=get_current_user(request, "id")),
        "l_types": Leave_Types.objects.all(),
        "l_balance": employee_record.balance,
        "gender": get_current_user(request, "gender")
    }

    return render(request, "leave/leave.html", context)


@login_required
def apply_leave(request):
    if request.method == "POST":

        user = request.user  # getting the current logged in user
        employee = user.solitonuser.employee
        department = Department.objects.get(pk=employee.organisationdetail.department.id)
        team = Team.objects.get(pk=employee.organisationdetail.team.id)

        # department_id = Department.objects.get(pk=department)

        l_type = Leave_Types.objects.get(pk=request.POST["ltype"])

        date_format = "%Y-%m-%d"
        s_date = request.POST["s_date"]
        e_date = request.POST["e_date"]

        # getting the leave type entitlement
        n_days = calculate_leave_days(s_date, e_date)
        l_days = l_type.leave_days

        if n_days <= l_days:
            new_balance = 0
            if l_type.leave_type == "Annual":
                curr_balance = employee.leave_balance
                new_balance = curr_balance - n_days

            if n_days <= new_balance:
                leave_app = LeaveApplication(employee=employee, leave_type=l_type, \
                start_date=s_date, end_date=e_date, no_of_days=n_days, \
                balance=curr_balance, department=department, \
                team=team)

                leave_app.save()

                subject = 'New Leave Request'
                from_mail = settings.EMAIL_HOST_USER
                msg = 'You have a new leave request that requires your attention'
                to_mails = [user.email, 'walusimbi96@gmail.com']

                # send_mail(subject, msg, from_mail, to_mails,fail_silently=False)

                messages.success(request, 'Leave Request Sent Successfully')

                return redirect('apply_leave_page')

            else:
                messages.warning(request, f'You have insufficient {l_type} leave Balance {n_days}')
                if str(user.solitonuser.soliton_role) == 'Employee':
                    context = {
                        "employee": user.solitonuser.employee,
                        "employee_leave_page": 'active'
                    }
                    return render(request, "leave/leave.html", context)
                else:
                    return render(request, "leave/leave.html")

        else:
            messages.warning(request, f'You cannot Request({n_days}) for more than the\
                {l_type.leave_type} leave days ({l_type.leave_days})')
            return render(request, "leave/leave.html")


def approve_leave(request):
    if request.method == "POST":
        user = request.user  # getting the current logged in User
        employee = user.solitonuser.employee
        role = get_current_user(request, "role")

        l_type = Leave_Types.objects.get(pk=request.POST.get("ltype"))
        n_days = request.POST.get("ndays")
        leave = LeaveApplication.objects.get(pk=request.POST["app_id"])
        leave_record = Leave_Records.objects. \
            filter(employee=employee, leave_year=date.today().year)

        is_supervisor = Team.objects.filter(id=get_current_user(request, "team"), \
                                            supervisors=get_current_user(request, "id")).count()

        
        if is_supervisor == 1: 
            print("User Id: ", get_current_user(request,"id"))
            print("User Team: ", get_current_user(request,"team"))
            LeaveApplication.objects.filter(pk=leave.id).update(supervisor=get_current_user(request, "id"),
                                                                supervisor_status="Approved", )

        elif user.is_hod:
            LeaveApplication.objects.filter(pk=leave.id).update(hod=get_current_user(request, "id"),
                                                                hod_status="Approved")

        elif user.is_hr:
            curr_balance = int(leave_record.balance)
            total_applied = int(leave_record.leave_applied)
            total_taken = int(leave_record.total_taken)

            if l_type.leave_type == "Annual":
                new_balance = int(curr_balance) - int(n_days)

                total_applied += 1
                total_taken += int(n_days)

            else:
                new_balance = curr_balance

            LeaveApplication.objects.filter(pk=leave.id).update(hr=get_current_user(request, "id"),
                hr_status="Approved", overall_status="Approved",balance=new_balance)

            leave_record.update(leave_applied=total_applied, total_taken=total_taken, \
                                balance=new_balance)
        else:
            messages.warning(request, 'Leave Approval Failed')
            return redirect('leave_dashboard_page')

        messages.success(request, 'Leave Approved Successfully')
        return redirect('leave_dashboard_page')


def leave_records(request):
    if not request.user.is_authenticated:
        return render(request, "ems_auth/login.html", {"message": None})

    current_year = date.today().year
    context = {
        "leave_page": "active",
        "leave_records": Leave_Records.objects.filter(leave_year=current_year),
        "current_year": current_year,
        "years": generate_years(),
    }
    return render(request, "leave/leave_records.html", context)


def add_leave_records(request):
    yr = 0

    if request.method == "POST":
        yr = request.POST["leave_yr"]
    
        leave_records = Leave_Records.objects.all()
        employees = Employee.objects.all()

        if not leave_records:
            for employee in employees:
                employee_name = employee.id

                leave_record = Leave_Records(employee=employee, leave_year=yr, \
                    entitlement=21, residue=0, leave_applied=0, total_taken=0, \
                    balance=21)

                leave_record.save()
            messages.success(request, f'Leave Records Generated for the Year - {yr}')
        else:
            year_count = leave_records.filter(leave_year=yr).count()

            entitlement = 21

            if year_count == 0:
                for employee in employees:
                    employee_name = employee.id

                    leave_balance = leave_records.get(employee=employee, leave_year=yr - 1)

                    balance = leave_balance.balance

                    residue = 0
                    if balance > 5:
                        residue = 5
                    else:
                        residue = balance

                    initial_balance = entitlement + residue

                    leave_record = Leave_Records(employee=employee, leave_year=yr, \
                                                entitlement=entitlement, residue=residue, leave_applied=0, total_taken=0, \
                                                balance=initial_balance)

                    leave_record.save()
                messages.success(request, f'Leave Records Generated for the Year - {yr}')
                                  
        context = {
        "leave_page": "active",
        "leave_records": Leave_Records.objects.filter(leave_year=yr),
        "years": generate_years()
    }
    return render(request, "leave/leave_records.html", context)

def generate_years():
    current_year = date.today().year

    next_years = []

    start_year = current_year - 3
    i = 0
    while i < 8:
        next_years.append(start_year + 1)
        start_year += 1
        i += 1
    
    return next_years

def calculate_leave_days(start_date, end_date):    
    date_format = "%Y-%m-%d"
    from_date = datetime.datetime.strptime(start_date, date_format)
    to_date = datetime.datetime.strptime(end_date, date_format)

    date_difference = to_date - from_date

    all_days_between = (date_difference.days + 1)

    holidays = Holidays.objects.filter(holiday_date__range=(from_date, to_date)).count()

    all_working_days = all_days_between - holidays
    k = 0
    while k <= all_days_between:
        check_date = from_date + datetime.timedelta(days=k)

        if check_date.weekday() == 6:
            all_working_days = all_working_days - 1

        k = k + 1

    return all_working_days


def annual_calendar(request):
    # first_day = calendar.TextCalendar(calendar.MONDAY)
    # annual_calendar = first_day.formatyear(2019)
    context = {
        "annual_calendar": "active",
        "employees": Employee.objects.all()
    }

    return render(request, 'leave/annual_calendar.html', context)


def leave_planer(request):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'registration/login.html', {"message": None})

    current_year = datetime.datetime.now().year

    context = {
        "leave_planner": "active",
        "planner": annual_planner.objects.all(),
        "leave_types": Leave_Types.objects.all(),
        "employees": Employee.objects.all(),
        "year": current_year
    }
    return render(request, 'leave/leave_planner.html', context)


def add_new_absence(request):
    if request.method == "POST":
        employee = Employee.objects.get(pk=request.user.id)
        leave = Leave_Types.objects.get(pk=request.POST["leave_type"])
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]

    date_format = "%Y-%m-%d"
    leave_year = datetime.datetime.strptime(from_date, date_format).year
    leave_month = calendar.month_name[datetime.datetime.strptime(from_date, date_format).month]
    leave_days = calculate_leave_days(from_date, to_date)

    try:
        if leave_days >= 1:
            planner = annual_planner(leave_year=leave_year, date_from=from_date, date_to=to_date, \
                                     employee=employee, leave=leave, leave_month=leave_month[0:3],
                                     no_of_days=leave_days)

            planner.save()

            messages.success(request, f'Data Saved Successfully')

            overlaps = get_leave_overlap(from_date, to_date)

            if overlaps > 1:
                messages.warning(request, f'There are {overlaps - 1} Overlap(s) during the selected period.\
                    \n Click to View Overlaps')

        else:
            messages.warning(request, f'Invalid Date Range')

        return redirect('leave_planner')

    except:
        messages.error(request, f'Data Not Saved, Check you inputs and try again!')

        #  return redirect('leave_planner')


def get_leave_overlap(start_date, end_date):
    absences = annual_planner.objects.all()

    Range = namedtuple('Range', ['start', 'end'])

    date_format = "%Y-%m-%d"
    from_date = datetime.datetime.strptime(start_date, date_format)
    to_date = datetime.datetime.strptime(end_date, date_format)

    r1 = Range(start=from_date.date(), end=to_date.date())

    overlap = 0
    overlap_count = 0
    for absence in absences:
        r2 = Range(start=absence.date_from, end=absence.date_to)
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)

        if overlap > 0:
            overlap_count += 1

    return overlap_count


def Leave_planner_summary(request):
    # The line requires the user to be authenticated before accessing the view responses.
    if not request.user.is_authenticated:
        # if the user is not authenticated it renders a login page
        return render(request, 'registration/login.html', {"message": None})

    department_id = 0
    team_id = 0
    if request.method == "POST":
        department_id = request.POST["department"]
        team_id = request.POST["team"]

    # Select multiple records
    all_plans = None
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT e.first_name || ' ' || e.last_name as Employee,\
        SUM(CASE WHEN leave_month = 'Jan' THEN no_of_days ELSE 0 END) as Jan,\
        SUM(CASE WHEN leave_month = 'Feb' THEN no_of_days ELSE 0 END) as Feb,\
        SUM(CASE WHEN leave_month = 'Mar' THEN no_of_days ELSE 0 END) as Mar,\
        SUM(CASE WHEN leave_month = 'Apr' THEN no_of_days ELSE 0 END) as Apr,\
        SUM(CASE WHEN leave_month = 'May' THEN no_of_days ELSE 0 END) as May,\
        SUM(CASE WHEN leave_month = 'Jun' THEN no_of_days ELSE 0 END) as Jun,\
        SUM(CASE WHEN leave_month = 'Jul' THEN no_of_days ELSE 0 END) as Jul,\
        SUM(CASE WHEN leave_month = 'Aug' THEN no_of_days ELSE 0 END) as Aug,\
        SUM(CASE WHEN leave_month = 'Sep' THEN no_of_days ELSE 0 END) as Sep,\
        SUM(CASE WHEN leave_month = 'Oct' THEN no_of_days ELSE 0 END) as Oct,\
        SUM(CASE WHEN leave_month = 'Nov' THEN no_of_days ELSE 0 END) as Nov,\
        SUM(CASE WHEN leave_month = 'Dec' THEN no_of_days ELSE 0 END) as Dec\
        FROM employees_employee e LEFT OUTER JOIN leave_annual_planner l ON e.id=l.employee_id\
		WHERE e.id IN \
            (SELECT employee_id FROM employees_organisationdetail \
                WHERE department_id={department_id} AND team_id={team_id})\
        GROUP BY e.id;")
        all_plans = cursor.fetchall()
    # DB API fetchall produces a list of tuples

    context = {
        "plans": all_plans,
        "departments": Departments.objects.all(),
        "teams": Teams.objects.all()
    }
    return render(request, 'leave/annual_calendar.html', context)


def leave_calendar(request, month=date.today().month, year=date.today().year):
    year = int(year)
    month = int(month)

    if year < 1900 or year > 2099:
        year = date.today().year

    month_name = calendar.month_name[month]

    cal = HTMLCalendar.formatmonth(year, month)

    context = {
        "title": year,
        "calendar": cal
    }
    return render(request, 'leave/leave_calendar.html', context)
