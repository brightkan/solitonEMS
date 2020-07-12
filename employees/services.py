from employees.models import Employee
from settings.models import Currency
from leave.models import Leave_Records
import datetime


def create_employee_instance(request):
    # Fetching data from the add new employee form
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    grade = request.POST['grade']
    basic_salary = request.POST['basic_salary']
    lunch_allowance = request.POST['lunch_allowance']
    gender = request.POST['gender']
    marital_status = request.POST['marital_status']
    start_date = request.POST['start_date']
    nationality = request.POST['nationality']
    nssf_no = request.POST['nssf_no']
    ura_tin = request.POST['ura_tin']
    national_id = request.POST['national_id']
    telephone = request.POST['telephone']
    residence_address = request.POST['residence_address']
    dob = request.POST['dob']
    renumeration_currency_id = request.POST['renumeration_currency']
    title = request.POST['title']
    work_station = request.POST['work_station']
    currency = Currency.objects.get(pk=renumeration_currency_id)
    # try:
    # Creating instance of Employee
    employee = Employee(first_name=first_name, last_name=last_name, basic_salary=basic_salary,
                        grade=grade, gender=gender,
                        marital_status=marital_status, start_date=start_date,
                        nationality=nationality, nssf_no=nssf_no,
                        ura_tin=ura_tin, national_id=national_id, telephone_no=telephone,
                        residence_address=residence_address, dob=dob, currency=currency, title=title,
                        work_station=work_station,
                        lunch_allowance=lunch_allowance
                        )
    # Saving the employee instance
    employee.save()

    add_leave_record(employee, start_date)

    return employee


def suspend(employee):
    employee.status = "Suspended"
    employee.save()
    return employee


def add_leave_record(employee, start_date):
    date_format = "%Y-%m-%d"
    begin_date = datetime.datetime.strptime(start_date, date_format)
    start_day = begin_date.day
    start_month = begin_date.month
    start_year = begin_date.year

    current_year = datetime.date.today().year

    leave_days = 21

    if start_year == current_year:
        if start_day >= 15:
            leave_days = (12 - start_month) * 1.75
        else:
            leave_days = (12 - (start_month - 1)) * 1.75

    leave_record = Leave_Records(
        employee=employee,
        leave_year=current_year,
        entitlement=leave_days,
        residue=0,
        leave_applied=0,
        total_taken=0,
        balance=leave_days
    )

    leave_record.save()


def add_employee_contacts(request):
    if request.method == "POST":
        contact_type = request.POST.get('contact_type')
        contacts = request.POST.get('contact')
        employee_id = request.POST.get('employee_id')

        employee = get_employee(employee_id)

        contact = Contact(contact_type=contact_type, contact=contacts, employee=employee)

        employee.save()
