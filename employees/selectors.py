from employees.models import Employee, Contacts
from settings.selectors import get_ugx_currency, get_usd_currency


def get_employee(employee_id):
    return Employee.objects.get(pk=employee_id)


def get_active_employees():
    return Employee.objects.filter(status='Active').order_by('start_date')


def get_passive_employees():
    return Employee.objects.filter(status='Suspended')


def get_employees_paid_in_ugx():
    ugx_currency = get_ugx_currency()
    return Employee.objects.filter(status="Active", currency=ugx_currency)


def get_employees_paid_in_usd():
    usd_currency = get_usd_currency()
    return Employee.objects.filter(status="Active", currency=usd_currency)


def get_employee_contacts(employee):
    return Contacts.objects.filter(employee=employee).order_by('contact_type')


def get_contact(contact_id):
    return Contacts.objects.get(pk=contact_id)
