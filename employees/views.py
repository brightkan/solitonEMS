from datetime import date

from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from employees.services import create_employee_instance, suspend, update_deduction
from ems_admin.decorators import log_activity
from ems_auth.decorators import ems_login_required, hr_required, first_login
from ems_auth.models import User
from organisation_details.models import Department, Position, Team, OrganisationDetail
from organisation_details.selectors import get_all_positions
from settings.selectors import get_all_currencies
from .models import (
    Employee,
    HomeAddress,
    Certification,
    EmergencyContact,
    Beneficiary,
    Spouse,
    Dependant,
    BankDetail, Allowance,
    Supervision,
    Deduction,
    Contacts)
from leave.models import Leave_Records

from settings.models import Currency
import csv

from notification.selectors import get_user_notifications
from .selectors import get_employee, get_active_employees, get_passive_employees, get_employee_contacts, get_contact
from leave.selectors import get_leave_record


@ems_login_required
@first_login
@log_activity
def dashboard_page(request):
    # Get the user
    user = request.user
    try:
        notifications = get_user_notifications(user)
        number_of_notifications = notifications.count()
        active_employees = get_active_employees()
        suspend_employees = get_passive_employees()
        number_of_employees = active_employees.count()

        context = {
            "user": user,
            "dashboard_page": "active",
            "number_of_employees": number_of_employees,
            "notifications": notifications,
            "number_of_notifications": number_of_notifications,
            "number_of_suspended": suspend_employees.count(),
        }

        return render(request, 'employees/dashboard.html', context)

    except User.DoesNotExist:
        return render(request, 'ems_auth/login.html', {"message": "Soliton User does not exist"})


@ems_login_required
@hr_required
@log_activity
def employees_page(request):
    all_currencies = get_all_currencies()
    active_employees = get_active_employees()
    context = {
        "user": request.user,
        "currencies": all_currencies,
        "employees_page": "active",
        "employees": active_employees,
    }
    return render(request, 'employees/employees.html', context)


@ems_login_required
def employee_page(request, id):
    employee = Employee.objects.get(pk=id)
    yr = date.today().year
    leave_record = ""
    try:
        leave_record = Leave_Records.objects.get(employee=employee.id, leave_year=yr)
    except:
        pass

    context = {
        "user": request.user,
        "employees_page": "active",
        "employee": employee,
        "certifications": employee.certification_set.all(),
        "emergency_contacts": employee.emergencycontact_set.all(),
        "beneficiaries": employee.beneficiary_set.all(),
        "spouses": employee.spouse_set.all(),
        "dependants": employee.dependant_set.all(),
        "deps": Department.objects.all(),
        "titles": Position.objects.all(),
        "teams": Team.objects.all(),
        "allowances": Allowance.objects.all(),
        "supervisee_options": Employee.objects.exclude(pk=employee.id),
        "supervisions": Supervision.objects.filter(supervisor=employee),
        "leave_record": leave_record,
        "contacts": get_employee_contacts(employee)
    }
    return render(request, 'employees/employee.html', context)


@ems_login_required
@log_activity
def edit_employee_page(request, id):
    employee = Employee.objects.get(pk=id)
    context = {
        "employees_page": "active",
        "employee": employee,
        "deps": Department.objects.all(),
        "titles": Position.objects.all(),
        "currencies": Currency.objects.all()
    }
    return render(request, 'employees/edit_employee.html', context)


@login_required
@log_activity
def edit_certification_page(request, id):
    user = request.user
    certification = Certification.objects.get(pk=id)
    context = {
        "user": user,
        "employees_page": "active",
        "certification": certification,
    }

    return render(request, 'employees/edit_cert.html', context)


@ems_login_required
@log_activity
def edit_emergency_contact_page(request, id):
    user = request.user
    emergency_contact = EmergencyContact.objects.get(pk=id)
    context = {
        "user": user,
        "employees_page": "active",
        "emergency_contact": emergency_contact,
    }

    return render(request, 'employees/edit_emergency.html', context)


# The login view authenticates the user
# The view also renders the login page


@ems_login_required
@log_activity
def edit_beneficiary_page(request, id):
    # redirect according to roles
    user = request.user
    beneficiary = Beneficiary.objects.get(pk=id)
    context = {
        "user": user,
        "employees_page": "active",
        "beneficiary": beneficiary,

    }

    return render(request, 'employees/edit_beneficiary.html', context)


@login_required
@log_activity
def edit_spouse_page(request, id):
    # redirect according to roles
    user = request.user
    spouse = Spouse.objects.get(pk=id)
    spouse.save()

    context = {
        "user": user,
        "employees_page": "active",
        "spouse": spouse
    }

    return render(request, 'employees/edit_spouse.html', context)


@ems_login_required
@hr_required
@log_activity
def edit_dependant_page(request, id):
    # redirect according to roles
    user = request.user
    dependant = Dependant.objects.get(pk=id)
    context = {
        "user": user,
        "employees_page": "active",
        "dependant": dependant,

    }

    return render(request, 'employees/edit_dependant.html', context)


###################################################################
# Processes
###################################################################
@login_required
@hr_required
@log_activity
def add_new_employee(request):
    if request.method == 'POST':
        employee = create_employee_instance(request)
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the employees" % employee.first_name,
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def delete_employee(request, id):
    try:
        # Grab the employee
        employee = Employee.objects.get(pk=id)

        name = employee.first_name + " " + employee.last_name
        # Delete the employee
        employee_to_delete = employee
        employee_to_delete.delete()

    except Employee.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The employee no longer exists on the system"
        }

        return render(request, 'employees/deleted_employee.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from employees" % (name),

    }
    return render(request, 'employees/deleted_employee.html', context)


@login_required
@hr_required
@log_activity
def edit_employee(request, id):
    if request.method == 'POST':
        # Fetching data from the add new employee form
        employee = Employee.objects.get(pk=id)
        employee.title = request.POST['title']
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.grade = request.POST['grade']
        employee.basic_salary = request.POST['basic_salary']
        employee.lunch_allowance = request.POST['lunch_allowance']
        employee.gender = request.POST['gender']
        employee.marital_status = request.POST['marital_status']
        employee.start_date = request.POST['start_date']
        employee.nationality = request.POST['nationality']
        employee.nssf_no = request.POST['nssf_no']
        employee.ura_tin = request.POST['ura_tin']
        employee.national_id = request.POST['national_id']
        employee.telephone_no = request.POST['telephone']
        employee.residence_address = request.POST['residence_address']
        employee.dob = request.POST['dob']
        currency_id = request.POST['renumeration_currency']
        employee.bonus = request.POST['bonus']
        employee.currency = Currency.objects.get(pk=currency_id)

        employee.status = request.POST['status']

        # Saving the employee instance
        employee.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's bio data" % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)



    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def add_new_home_address(request):
    if request.method == 'POST':
        # Fetching data from the add new home address form
        employee_id = request.POST['employee_id']
        division = request.POST['division']
        district = request.POST['district']
        county = request.POST['county']
        sub_county = request.POST['sub_county']
        parish = request.POST['parish']
        village = request.POST['village']
        address = request.POST['address']
        telephone = request.POST['telephone']

        employee = Employee.objects.get(pk=employee_id)
        # Creating instance of Home Address
        homeaddress = HomeAddress(employee=employee, district=district, division=division, county=county,
                                  sub_county=sub_county,
                                  parish=parish, village=village, address=address, telephone=telephone)
        # Saving the Home Address instance
        homeaddress.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added Home Address to the %s's details" % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def add_bank_details(request):
    if request.method == 'POST':
        # Fetching data from the add new home address form
        employee_id = request.POST['employee_id']
        name_of_bank = request.POST['bank_name']
        branch = request.POST['bank_branch']
        bank_account = request.POST['bank_account']

        # Get the employee instance
        employee = Employee.objects.get(pk=employee_id)
        # Creating instance of Bank Detail
        bank_detail = BankDetail(employee=employee, name_of_bank=name_of_bank, branch=branch, bank_account=bank_account)
        # Saving the BankDetail instance
        bank_detail.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s Bank Details " % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def add_organisation_details(request):
    if request.method == 'POST':
        # Fetching data from the add new home address form
        employee_id = request.POST['employee_id']
        depart = request.POST['depart']
        position = request.POST['position']
        team = request.POST['team']

        # Get the employee instance
        employee = Employee.objects.get(pk=employee_id)
        # Get the department instance
        department = Department.objects.get(pk=depart)
        # Get the Job title instance
        team = Team.objects.get(pk=team)
        position = Position.objects.get(pk=position)
        # Creating instance of organisation Detail
        organisation_detail = OrganisationDetail(employee=employee, department=department,
                                                 position=position, team=team)
        # Saving the BankDetail instance
        organisation_detail.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s Organisation Details " % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def edit_organisation_details(request):
    if request.method == 'POST':
        # Fetching data from the add new home address form
        employee_id = request.POST['employee_id']
        depart = request.POST['depart']
        position = request.POST['position']
        team = request.POST['team']

        # Get the employee instance
        employee = Employee.objects.get(pk=employee_id)
        # Get the department instance
        department = Department.objects.get(pk=depart)
        team = Team.objects.get(pk=team)
        position = Position.objects.get(pk=position)
        # get instance of organisation Detail
        organisation_detail = OrganisationDetail.objects.get(employee=employee)
        organisation_detail.department = department
        organisation_detail.position = position
        organisation_detail.team = team
        # Saving the BankDetail instance
        organisation_detail.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s Organisation Details " % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
@hr_required
@log_activity
def edit_home_address(request):
    if request.method == 'POST':
        # Fetch the employee
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)
        # Grab the home address
        home_address = HomeAddress.objects.get(employee=employee)

        home_address.district = request.POST['district']
        home_address.division = request.POST['division']
        home_address.county = request.POST['county']
        home_address.sub_county = request.POST['sub_county']
        home_address.parish = request.POST['parish']
        home_address.village = request.POST['village']
        home_address.address = request.POST['address']
        home_address.telephone = request.POST['telephone']

        # Saving the home address instance
        home_address.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's home address" % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@ems_login_required
@hr_required
@log_activity
def edit_bank_details(request):
    if request.method == 'POST':
        # Fetching data from the edit home address form

        # Fetch the employee
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)
        # Grab the Bankdetail
        bank_detail = BankDetail.objects.get(employee=employee)

        bank_detail.name_of_bank = request.POST['bank_name']
        bank_detail.branch = request.POST['bank_branch']
        bank_detail.bank_account = request.POST['bank_account']

        # Saving the bank detail instance
        bank_detail.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's Bank Details" % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@hr_required
@log_activity
def add_certification(request):
    if request.method == 'POST':
        # Fetching data from the add new employee form
        institution = request.POST['institution']
        year_completed = request.POST['year_completed']
        certification = request.POST['certification']
        grade = request.POST['grade']
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of Certification
        certification = Certification(employee=employee, institution=institution, year_completed=year_completed,
                                      name=certification,
                                      grade=grade)
        # Saving the certification instance
        certification.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the certifications" % (certification.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def edit_certification(request):
    if request.method == 'POST':

        # Fetch the certification id
        cert_id = request.POST['cert_id']

        # Grab the certification
        certification = Certification.objects.get(pk=cert_id)
        certification.institution = request.POST['institution']
        certification.year_completed = request.POST['year_completed']
        certification.name = request.POST['name']
        certification.grade = request.POST['grade']

        # Saving the certification instance
        certification.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's certification" % (certification.employee.first_name),
            "employee": certification.employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@ems_login_required
@hr_required
@log_activity
def delete_certification(request, id):
    try:
        # Grab the certification
        certification = Certification.objects.get(pk=id)

        name = certification.name
        employee = certification.employee
        # Delete the certification
        certification.delete()

    except Certification.DoesNotExist:
        context = {
            "employees_page": "active",
            "employee": employee,
            "deleted_msg": "The certification no longer exists on the system",

        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "employee": employee,
        "deleted_msg": "You have deleted %s from certifications" % (name)
    }
    return render(request, 'employees/deleted.html', context)


@hr_required
@log_activity
def add_emergency_contact(request):
    if request.method == 'POST':
        # Fetching data from the add new employee form
        name = request.POST['name']
        relationship = request.POST['relationship']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        employee_id = request.POST['employee_id']

        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of EmergencyContact
        emergency_contact = EmergencyContact(employee=employee, name=name, relationship=relationship,
                                             mobile_number=mobile_number, email=email)
        # Saving the certification instance
        emergency_contact.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the emergency contacts" % (emergency_contact.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@hr_required
@log_activity
def delete_emergency_contact(request, id):
    try:
        # Grab the emergency contact
        emergency_contact = EmergencyContact.objects.get(pk=id)
        name = emergency_contact.name
        employee = emergency_contact.employee
        # Delete the certification
        emergency_contact.delete()

    except EmergencyContact.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The emergency contact no longer exists on the system",
            "employee": employee
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from emergency contacts" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def edit_emergency_contact(request):
    if request.method == 'POST':

        # Fetch the emergency contact id
        emergency_id = request.POST['emergency_id']

        # Grab the EmergencyContact
        emergency_contact = EmergencyContact.objects.get(pk=emergency_id)

        emergency_contact.name = request.POST['name']
        emergency_contact.relationship = request.POST['relationship']
        emergency_contact.mobile_number = request.POST['mobile_number']
        emergency_contact.email = request.POST['email']

        # Saving the EmergencyContact instance
        emergency_contact.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's emergency contact" % (
                emergency_contact.employee.first_name),
            "employee": emergency_contact.employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def add_beneficiary(request):
    if request.method == 'POST':
        # Fetching data from the add new employee form
        name = request.POST['name']
        relationship = request.POST['relationship']
        percentage = request.POST['percentage']
        mobile_number = request.POST['mobile_number']
        employee_id = request.POST['employee_id']

        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of Beneficiary
        beneficiary = Beneficiary(employee=employee, name=name, relationship=relationship,
                                  mobile_number=mobile_number, percentage=percentage)

        # Saving the certification instance
        beneficiary.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the emergency beneficiaries" % (beneficiary.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def edit_beneficiary(request):
    if request.method == 'POST':

        # Fetch the beneficiary id
        beneficiary_id = request.POST['beneficiary_id']

        # Grab the EmergencyContact
        beneficiary = Beneficiary.objects.get(pk=beneficiary_id)

        beneficiary.name = request.POST['name']
        beneficiary.relationship = request.POST['relationship']
        beneficiary.mobile_number = request.POST['mobile_number']
        beneficiary.percentage = request.POST['percentage']

        # Saving the EmergencyContact instance
        beneficiary.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's beneficiary details" % (beneficiary.employee.first_name),
            "employee": beneficiary.employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@login_required
def delete_beneficiary(request, id):
    try:
        # Grab the Beneficiary
        beneficiary = Beneficiary.objects.get(pk=id)

        name = beneficiary.name
        employee = beneficiary.employee
        # Delete the Beneficiary
        beneficiary.delete()

    except Beneficiary.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The beneficiary no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from beneficiaries" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def add_spouse(request):
    if request.method == 'POST':
        # Fetching data from the add new employee form
        name = request.POST['name']
        national_id = request.POST['national_id']
        dob = request.POST['dob']
        occupation = request.POST['occupation']
        telephone = request.POST['telephone']
        nationality = request.POST['nationality']
        passport_number = request.POST['passport_number']
        alien_certificate_number = request.POST['alien_certificate_number']
        immigration_file_number = request.POST['immigration_file_number']
        employee_id = request.POST['employee_id']

        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of Spouse
        spouse = Spouse(employee=employee, name=name, national_id=national_id, dob=dob, occupation=occupation,
                        telephone=telephone, nationality=nationality, passport_number=passport_number,
                        alien_certificate_number=alien_certificate_number,
                        immigration_file_number=immigration_file_number)
        # Saving the Spouse instance
        spouse.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the spouses" % (spouse.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def delete_spouse(request, id):
    try:
        # Grab the Spouse
        spouse = Spouse.objects.get(pk=id)

        name = spouse.name
        employee = spouse.employee
        # Delete the Spouse
        spouse.delete()

    except Spouse.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The spouse no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from the spouses" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def edit_spouse(request):
    if request.method == 'POST':
        # Fetch the spouse id
        spouse_id = request.POST['spouse_id']

        # Grab the Spouse
        spouse = Spouse.objects.get(pk=spouse_id)
        spouse.name = request.POST['name']
        spouse.national_id = request.POST['national_id']
        spouse.dob = request.POST['dob']
        spouse.occupation = request.POST['occupation']
        spouse.telephone = request.POST['telephone']
        spouse.nationality = request.POST['nationality']
        spouse.passport_number = request.POST['passport_number']
        spouse.alien_certificate_number = request.POST['alien_certificate_number']
        spouse.immigration_file_number = request.POST['immigration_file_number']

        # Saving the Spouse instance
        spouse.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's spouse details" % (spouse.employee.first_name),
            "employee": spouse.employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def add_dependant(request):
    if request.method == 'POST':
        # Fetching data from the add dependants' form
        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']

        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of Dependent
        dependant = Dependant(employee=employee, name=name,
                              dob=dob, gender=gender)

        # Saving the Dependant instance
        dependant.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the dependants" % (dependant.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def edit_dependant(request):
    if request.method == 'POST':
        # Fetch the dependant id
        dependant_id = request.POST['dependant_id']

        # Grab the Dependant
        dependant = Dependant.objects.get(pk=dependant_id)

        dependant.name = request.POST['name']
        dependant.dob = request.POST['dob']
        dependant.gender = request.POST['gender']

        # Saving the Dependant instance
        dependant.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s's dependant details" % (dependant.employee.first_name),
            "employee": dependant.employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def delete_dependant(request, id):
    try:
        # Grab the Dependant
        dependant = Dependant.objects.get(pk=id)

        name = dependant.name
        employee = dependant.employee
        # Delete the Dependent
        dependant.delete()

    except Dependant.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The dependant no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from the dependents" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def add_deduction(request):
    if request.method == 'POST':
        # Fetching data from the add deductions' form
        sacco = request.POST['sacco']
        damage = request.POST['damage']
        salary_advance = request.POST['salary_advance']
        police_fine = request.POST['police_fine']

        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)

        try:
            deduction = Deduction.objects.create(
                employee=employee,
                sacco=sacco,
                damage=damage,
                salary_advance=salary_advance,
                police_fine=police_fine
            )
            messages.success(request, "Successfully added sacco deduction")
            return HttpResponseRedirect(reverse(add_more_details_page, args=[employee_id]))

        except IntegrityError:
            messages.error(request, "Integrity problems while adding deduction")
            return HttpResponseRedirect(reverse(add_more_details_page, args=[employee_id]))

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@ems_login_required
@log_activity
def edit_deduction(request):
    if request.POST:
        try:
            sacco = request.POST['sacco']
            damage = request.POST['damage']
            salary_advance = request.POST['salary_advance']
            police_fine = request.POST['police_fine']
            employee_id = request.POST['employee_id']
            employee = Employee.objects.get(pk=employee_id)

            deduction = update_deduction(employee=employee,
                                         sacco=sacco,
                                         damage=damage,
                                         salary_advance=salary_advance,
                                         police_fine=police_fine)
            messages.success(request, "Deduction updated successfully")
            return HttpResponseRedirect(reverse(add_more_details_page, args=[employee_id]))
        except IntegrityError:
            messages.error(request, "Integrity problems while adding deduction")
            return HttpResponseRedirect(reverse(add_more_details_page, args=[employee_id]))

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def add_allowance(request):
    if request.method == 'POST':
        # Fetching data from the add allowances form
        name = request.POST['allowance_name']
        amount = request.POST['allowance_amount']
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(pk=employee_id)

        # Creating instance of Allowance
        allowance = Allowance(employee=employee, name=name, amount=amount)

        # Saving the Allowance instance
        allowance.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the allowances" % (allowance.name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)


    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def delete_deduction(request, id):
    try:
        # Grab the Deduction
        deduction = Deduction.objects.get(pk=id)

        name = deduction.name
        employee = deduction.employee
        # Delete the deduction
        deduction.delete()

    except Deduction.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The deduction no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from the deductions" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def edit_leave_details(request):
    if request.method == 'POST':
        # Fetching data from the edit leave' form
        employee = Employee.objects.get(pk=request.POST['employee_id'])
        entitlement = request.POST['entitlement']
        balance = request.POST['leave_balance']
        residue = request.POST['residue']
        no_of_leaves = request.POST['no_of_leaves']
        total_taken = request.POST['total_taken']

        leave_record = get_leave_record(employee)

        if leave_record:
            leave_record.entitlement = entitlement
            leave_record.residue = residue
            leave_record.leave_applied = no_of_leaves
            leave_record.total_taken = total_taken
            leave_record.balance = balance

            leave_record.save()
        else:
            leave_record = Leave_Records(
                employee=employee,
                leave_year=date.today().year,
                entitlement=entitlement,
                residue=residue, balance=balance,
                leave_applied=no_of_leaves,
                total_taken=total_taken
            )

            leave_record.save()

        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added leave records",
        }
        return HttpResponseRedirect(reverse('employee_page', args=[employee_id]))


@log_activity
def delete_allowance(request, id):
    try:
        # Grab the Allowance
        allowance = Allowance.objects.get(pk=id)

        name = allowance.name
        employee = allowance.employee
        # Delete the Allowance
        allowance.delete()

    except Allowance.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The allowance no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from the allowances" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@log_activity
def add_supervisee(request):
    if request.method == 'POST':
        # Fetching data from the add deductions' form
        supervisee_id = request.POST['supervisee_id']
        employee_id = request.POST['employee_id']

        # Fetch employee instance
        employee = Employee.objects.get(pk=employee_id)

        # Fetch employee instance of type supervisee
        supervisee = Employee.objects.get(pk=supervisee_id)

        # Create instance of supervision
        supervision = Supervision(supervisee=supervisee, supervisor=employee)
        # Save supervision instance
        supervision.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully added %s to the supervisees" % (supervision.supervisee),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)


@log_activity
def delete_supervisee(request, id):
    try:
        # Grab the supervision
        supervision = Supervision.objects.get(pk=id)

        name = supervision.supervisee.first_name
        employee = supervision.supervisor
        # Delete the Allowance
        supervision.delete()

    except Supervision.DoesNotExist:
        context = {
            "employees_page": "active",
            "deleted_msg": "The supervisee no longer exists on the system"
        }

        return render(request, 'employees/deleted.html', context)

    context = {
        "employees_page": "active",
        "deleted_msg": "You have deleted %s from the supervisees" % (name),
        "employee": employee
    }
    return render(request, 'employees/deleted.html', context)


@login_required
def employees_download(request):
    # Get all the associated Employee objects
    employees = Employee.objects.all()
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    filename = "employees.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    heading_text = "Soliton Employees"
    writer.writerow([heading_text.upper()])
    writer.writerow(
        ['ID', 'Title', 'Name', 'Workstation', 'Status', 'Renumeration Currency', 'Basic Salary', 'Grade', 'Gender',
         'Hired Date', 'Marital Status', 'Date of Birth', 'Nationality', 'NSSF NO.', 'Telephone', 'Residence Adddress',
         'National ID', 'URA TIN'])
    # Writing other rows
    for employee in employees:
        name = employee.first_name + " " + employee.last_name
        writer.writerow([employee.id, employee.title, name, employee.work_station, employee.status, employee.currency,
                         employee.basic_salary, employee.grade, employee.gender, employee.start_date,
                         employee.marital_status, employee.dob, employee.nationality, employee.nssf_no,
                         employee.telephone_no, employee.residence_address, employee.national_id, employee.ura_tin])

    # Return the response
    return response


@log_activity
def suspend_employee(request, employee_id):
    employee = get_employee(employee_id)
    suspend(employee)
    return HttpResponseRedirect(reverse('employees_page'))


def employee_profile_page(request, employee_id):
    employee = get_employee(employee_id)
    context = {
        "user": request.user,
        "employees_page": "active",
        "employee": employee,
    }

    return render(request, 'employees/employee_profile.html', context)


@log_activity
def add_more_details_page(request, employee_id):
    employee = get_employee(employee_id)
    positions = get_all_positions()
    context = {
        "user": request.user,
        "employees_page": "active",
        "employee": employee,
        "certifications": employee.certification_set.all(),
        "emergency_contacts": employee.emergencycontact_set.all(),
        "beneficiaries": employee.beneficiary_set.all(),
        "spouses": employee.spouse_set.all(),
        "dependants": employee.dependant_set.all(),
        "deps": Department.objects.all(),
        "titles": Position.objects.all(),
        "teams": Team.objects.all(),
        "allowances": Allowance.objects.all(),
        "supervisee_options": Employee.objects.exclude(pk=employee.id),
        "supervisions": Supervision.objects.filter(supervisor=employee),
        "positions": positions,
    }

    return render(request, 'employees/add_more_details.html', context)


@log_activity
def activate_employees_page(request):
    passive_employees = Employee.objects.exclude(status="Active")
    context = {
        "user": request.user,
        "employees_page": "active",
        "employees": passive_employees
    }
    return render(request, 'employees/activate_employees.html', context)


@log_activity
def activate_employee(request, employee_id):
    employee = get_employee(employee_id)
    employee.status = "Active"
    employee.save()
    messages.success(request, "Employee activated")
    return HttpResponseRedirect(reverse('activate_employees_page'))


@log_activity
def add_employee_contacts(request):
    if request.method == "POST":
        contact_type = request.POST.get('contact_type')
        contacts = request.POST.get('contact')
        employee_id = request.POST.get('employee_id')

        employee = get_employee(employee_id)

        contact = Contacts(contact_type=contact_type, contact=contacts, employee=employee)

        contact.save()

        messages.success(request, "Employee Contact Info saved Successfully")

        return JsonResponse({'success': True})
        # , 'redirect': "employee_page"


def delete_employee_contact(request):
    contact_id = request.POST.get('contact_id')
    contact = get_contact(contact_id)
    contact.delete()

    messages.success(request, 'Contact Deleted')

    return JsonResponse({'success': True})
