import csv
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from payroll.selectors import get_payroll_record_by_id
from payroll.services import create_payslip_list_service
from .models import PayrollRecord, Payslip
from django.urls import reverse
from .simple_payslip import SimplePayslip
from employees.models import Employee
from .procedures import get_total_non_statutory_deductions, get_total_nssf, get_total_paye, get_total_gross_pay, \
    get_total_basic_pay, \
    get_total_net_pay, render_to_pdf


def payroll_page(request):
    context = {
        "payroll_page": "active"
    }
    return render(request, 'payroll/payroll_page.html', context)


def manage_payroll_records_page(request):
    context = {
        "user": request.user,
        "payroll_page": "active",
        "payroll_records": PayrollRecord.objects.all(),
    }
    return render(request, 'payroll/payroll_records.html', context)


def payroll_record_page(request, id):
    # Get the payroll record
    payroll_record = PayrollRecord.objects.get(pk=id)

    month = payroll_record.month
    year = payroll_record.year

    # Get all the associated payslip objects
    payslips = Payslip.objects.filter(payroll_record=payroll_record)
    # Get all employees
    employees = Employee.objects.all()

    # Get the notifications
    user = request.user

    context = {
        "payroll_page": "active",
        "month": month,
        "year": year,
        "payrolls": payslips,
        "payroll_record": payroll_record,
        "total_nssf_contribution": get_total_nssf(payslips),
        "total_paye": get_total_paye(payslips),
        "total_gross_pay": get_total_gross_pay(payslips),
        "total_basic_pay": get_total_basic_pay(employees),
        "total_net_pay": get_total_net_pay(payslips),
    }
    return render(request, 'payroll/payroll_record.html', context)


def edit_period_page(request, id):
    # fetch PayrollRecordRequest 
    payroll_record = PayrollRecord.objects.get(pk=id)

    # Get the notifications
    user = request.user
    context = {
        "payroll_record": payroll_record,
        "payroll_page": "active",
    }

    return render(request, 'payroll/edit_payroll.html', context)


def payslip_page(request, id):
    # Get the payroll
    payslip = Payslip.objects.get(pk=id)
    # Get the notifications
    user = request.user

    context = {
        "payroll_page": "active",
        "payslip": payslip,
        "month": payslip.payroll_record.month,
        "year": payslip.payroll_record.year,
        "name_of_employee": "{} {}".format(payslip.employee.first_name, payslip.employee.last_name),
    }

    return render(request, 'payroll/payslip.html', context)


def generate_payslip_pdf(request, id):
    # Get the payslip
    payslip = Payslip.objects.get(pk=id)
    user = request.user
    context = {
        "payslip": payslip,
        "month": payslip.payroll_record.month,
        "year": payslip.payroll_record.year,
        "name_of_employee": "{} {}".format(payslip.employee.first_name, payslip.employee.last_name),
        "user": user
    }

    pdf = render_to_pdf('solitonems/payslip.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


###############################################################
# Processes
###############################################################

def add_period(request):
    # Fetch data from the add period form
    month = request.POST['month']
    year = request.POST['year']
    # Create payroll instance
    payroll_record = PayrollRecord(month=month, year=year)
    # Save payroll
    payroll_record.save()

    return HttpResponseRedirect(reverse('payroll_records_page'))


def delete_period(request, id):
    # Grab the payroll record
    payroll_record = PayrollRecord.objects.get(pk=id)
    # Delete the payrool_record
    payroll_record.delete()
    return HttpResponseRedirect(reverse('payroll_records_page'))


def edit_period(request):
    # Fetch values
    payroll_record_id = request.POST['payroll_record_id']
    month = request.POST['month']
    year = request.POST['year']
    # Fetch the PayrollRecord
    payroll_record = PayrollRecord(pk=payroll_record_id)
    # Overwrite old values
    payroll_record.month = month
    payroll_record.year = year
    # Save payroll record
    payroll_record.save()

    return HttpResponseRedirect(reverse('payroll_records_page'))


def create_payroll_payslips(request, id):
    payroll_record = get_payroll_record_by_id(id)
    create_payslip_list_service(payroll_record)
    return HttpResponseRedirect(reverse('payroll_record_page', args=[payroll_record.id]))


def add_prorate(request):
    # Fetch values from the form
    num_of_days_worked = request.POST['no_of_days_worked']
    payroll_id = request.POST['payroll_id']

    # Grab the Payroll object
    payroll = Payslip.objects.get(pk=payroll_id)

    # Grab the basic salary
    basic_salary = payroll.employee.basic_salary

    # Create the EmployeePayroll object
    employee_payroll = SimplePayslip(basic_salary)

    # Check if the the payroll has bonus and overtime
    if payroll.bonus:
        employee_payroll.gross_salary = employee_payroll.gross_salary + int(payroll)

    if payroll.overtime:
        if payroll.overtime == '0.0':
            employee_payroll.add_overtime_amount(0)
        else:
            employee_payroll.add_overtime_amount(payroll.overtime)

    # Add prorate to the employee payroll object
    employee_payroll.add_prorate(num_of_days_worked)

    # Subtract the deductions
    employee = payroll.employee

    total_deduction = get_total_non_statutory_deductions(employee)

    employee_payroll.deduct_amount_from_net_salary(total_deduction)

    # Update the payroll object 
    payroll.prorate = employee_payroll.prorate
    payroll.employee_nssf = int(employee_payroll.nssf_contrib)
    payroll.employer_nssf = int(employee_payroll.employer_nssf_contrib)
    payroll.gross_salary = int(employee_payroll.gross_salary)
    payroll.paye = int(employee_payroll.paye)
    payroll.net_salary = int(employee_payroll.net_salary)
    payroll.total_nssf_contrib = int(payroll.employee_nssf) + int(payroll.employer_nssf)
    payroll.total_statutory = payroll.total_nssf_contrib + int(payroll.paye)

    # Save the payroll object
    payroll.save()

    return HttpResponseRedirect(reverse('payslip_page', args=[payroll.id]))


def add_bonus(request):
    # Fetch values from the form
    bonus = request.POST['bonus']
    payroll_id = request.POST['payroll_id']

    # Grab the Payroll object
    payroll = Payslip.objects.get(pk=payroll_id)

    # Grab the basic salary
    basic_salary = payroll.employee.basic_salary

    # Create the EmployeePayroll object
    employee_payroll = SimplePayslip(basic_salary)

    # Check if the overtime is set
    if payroll.overtime:
        employee_payroll.add_overtime_amount(float(payroll.overtime))

    # Add bonus to the employee payroll object
    employee_payroll.add_bonus(bonus)

    # Subtract the deductions
    employee = payroll.employee

    total_deduction = get_total_non_statutory_deductions(employee)

    employee_payroll.deduct_amount_from_net_salary(total_deduction)

    # Update the payroll object
    payroll.bonus = employee_payroll.bonus
    payroll.employee_nssf = int(employee_payroll.nssf_contrib)
    payroll.employer_nssf = int(employee_payroll.employer_nssf_contrib)
    payroll.gross_salary = int(employee_payroll.gross_salary)
    payroll.paye = int(employee_payroll.paye)
    payroll.net_salary = int(employee_payroll.net_salary)
    payroll.total_nssf_contrib = int(payroll.employee_nssf) + int(payroll.employer_nssf)
    payroll.total_statutory = payroll.total_nssf_contrib + int(payroll.paye)

    # Save the payroll object 
    payroll.save()

    return HttpResponseRedirect(reverse('payslip_page', args=[payroll.id]))


def add_overtime(request):
    # Fetch values from the form
    number_of_hours_normal = request.POST['number_of_hours_normal']
    number_of_hours_holidays = request.POST['number_of_hours_holidays']
    payroll_id = request.POST['payroll_id']

    # Grab the Payroll object
    payroll = Payslip.objects.get(pk=payroll_id)

    # If the payroll already has bonus
    if float(payroll.bonus) > 0:
        context = {
            "payroll_page": "active",
            "payroll": payroll
        }
        return render(request, 'payroll/failed.html', context)

    # Grab the basic salary
    basic_salary = payroll.employee.basic_salary

    # Create the EmployeePayroll object
    employee_payroll = SimplePayslip(basic_salary)

    # Add overtime to the employee payroll object
    total_overtime = 0
    if number_of_hours_normal:
        overtime = employee_payroll.add_overtime(int(number_of_hours_normal), False)
        total_overtime = total_overtime + overtime

    if number_of_hours_holidays:
        overtime = employee_payroll.add_overtime(int(number_of_hours_holidays), True)
        total_overtime = total_overtime + overtime

    # Subtract the deductions
    employee = payroll.employee

    total_deduction = get_total_non_statutory_deductions(employee)

    # Update the payroll object
    payroll.gross_salary = int(employee_payroll.gross_salary)
    payroll.overtime = int(total_overtime)
    payroll.employee_nssf = int(employee_payroll.get_nssf_contrib(payroll.gross_salary))
    payroll.employer_nssf = int(employee_payroll.get_employer_nssf_contrib(payroll.gross_salary))
    payroll.paye = int(employee_payroll.get_paye(payroll.gross_salary))
    employee_payroll.get_net_salary(payroll.gross_salary)
    employee_payroll.deduct_amount_from_net_salary(total_deduction)
    payroll.net_salary = int(employee_payroll.net_salary)
    payroll.total_nssf_contrib = int(payroll.employee_nssf) + int(payroll.employer_nssf)
    payroll.total_statutory = payroll.total_nssf_contrib + int(payroll.paye)

    # Save the payroll object
    payroll.save()

    return HttpResponseRedirect(reverse('payslip_page', args=[payroll.id]))


def payroll_download(request, id):
    # Get the payroll record
    payroll_record = PayrollRecord.objects.get(pk=id)
    month = payroll_record.month
    year = payroll_record.year
    # Get all the associated Payroll objects
    payrolls = Payslip.objects.filter(payroll_record=payroll_record)
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    filename = "payroll_" + month + "_" + year + ".csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    heading_text = "Payroll for " + month + " " + year
    writer.writerow([heading_text.upper()])
    writer.writerow(
        ['Name', 'Employee NSSF Contribution', 'Employer NSSF contribution', 'PAYE', 'Bonus', 'Sacco Deduction',
         'Damage Deduction', 'Basic Salary', 'Lunch Allowance', 'Overtime', 'Gross Salary', 'Net Salary'])
    # Writing other rows
    for payroll in payrolls:
        name = payroll.employee.first_name + " " + payroll.employee.last_name
        writer.writerow(
            [name, payroll.employee_nssf, payroll.employer_nssf, payroll.paye, payroll.bonus, payroll.sacco_deduction,
             payroll.damage_deduction, payroll.employee.basic_salary, 150000, payroll.overtime, payroll.gross_salary,
             payroll.net_salary, ])

    # Return the response
    return response
