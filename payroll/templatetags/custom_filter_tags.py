from django import template

from employees.models import Deduction
from employees.selectors import get_employee

register = template.Library()


@register.filter
def currency_filter(value):
    """Outputs comma separated rounded off figure"""
    number = float(value)
    rounded_number = round(number)
    integer_number = int(rounded_number)
    return "{:,}".format(integer_number)


@register.filter
def sacco_filter(value: int):
    """Outputs integer with sacco dedution"""
    employee = get_employee(value)
    try:
        deduction = Deduction.objects.get(name="Sacco", employee=employee)
        amount = int(deduction.amount)
    except Deduction.DoesNotExist:
        deduction = 0
        amount = deduction
    return amount


@register.filter
def damage_filter(value: int):
    """Outputs integer with damage dedution"""
    employee = get_employee(value)
    try:
        deduction = Deduction.objects.get(name="Damage", employee=employee)
        amount = int(deduction.amount)
    except Deduction.DoesNotExist:
        deduction = 0
        amount = deduction
    return amount
