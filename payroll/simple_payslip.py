# Class for employee payroll
from employees.models import Employee, Deduction, StatutoryDeduction


def convert_to_zero_if_none(value):
    if value:
        return int(value)
    else:
        return 0


def calculate_employee_nssf_contribution(gross_salary):
    nssf_contribution = 0.05 * gross_salary
    return nssf_contribution


def calculate_employer_nssf_contribution(gross_salary):
    nssf_contribution = 0.10 * gross_salary
    return nssf_contribution


def calculate_paye(gross_salary, currency_cost) -> float:
    """Return paye in user currency"""
    # Assume the base currency is Uganda Shillings
    gross_salary_ugx = gross_salary * currency_cost

    if gross_salary_ugx < 235000:
        paye = 0

    elif 235000 < gross_salary_ugx < 335000:
        paye = 0.1 * (gross_salary - (235000 / currency_cost)) + (10000 / currency_cost)

    elif 335000 < gross_salary_ugx < 410000:
        paye = 0.2 * (gross_salary - (335000 / currency_cost)) + (10000 / currency_cost)

    elif 10000000 > gross_salary_ugx > 410000:
        paye = 0.3 * (gross_salary - (410000 / currency_cost)) + (25000 / currency_cost)

    else:
        """If gross salary is greater than 10 million"""
        paye = 0.3 * (gross_salary - (410000 / currency_cost)) + (25000 / currency_cost) + (
                gross_salary - (10000000 / currency_cost)) * 0.1

    return paye


def get_local_service_tax_deduction(employee):
    try:
        local_service_tax_deduction = employee.statutorydeduction.local_service_tax
    except StatutoryDeduction.DoesNotExist:
        local_service_tax_deduction = 0

    return local_service_tax_deduction


def get_sacco_deduction_amount(employee):
    try:
        sacco_deduction = employee.deduction.sacco
    except Deduction.DoesNotExist:
        sacco_deduction = 0

    return sacco_deduction


def get_damage_deduction_amount(employee):
    try:
        damage_deduction = employee.deduction.damage
    except Deduction.DoesNotExist:
        damage_deduction = 0

    return damage_deduction


def get_salary_advance_deduction_amount(employee):
    try:
        salary_advance_deduction = employee.deduction.salary_advance
    except Deduction.DoesNotExist:
        salary_advance_deduction = 0

    return salary_advance_deduction


def get_police_fine_deduction_amount(employee):
    try:
        police_fine_deduction = employee.deduction.police_fine
    except Deduction.DoesNotExist:
        police_fine_deduction = 0

    return police_fine_deduction


class SimplePayslip:

    def __init__(self, employee: Employee, overtime_pay=None, bonus=None):
        self.employee = employee
        self.overtime_pay = convert_to_zero_if_none(overtime_pay)
        self.bonus = convert_to_zero_if_none(bonus)
        self.local_service_tax = convert_to_zero_if_none(employee.local_service_tax)
        self.local_service_tax_deduction = get_local_service_tax_deduction(employee)
        self.gross_salary = self.sum_all_income(employee)
        self.employee_nssf = calculate_employee_nssf_contribution(self.gross_salary)
        self.employer_nssf = calculate_employer_nssf_contribution(self.gross_salary)
        self.currency_cost = float(self.employee.currency.cost)
        self.paye = calculate_paye(self.gross_salary, self.currency_cost)
        self.sacco_deduction_amount = get_sacco_deduction_amount(employee)
        self.damage_deduction_amount = get_damage_deduction_amount(employee)
        self.salary_advance_amount = get_salary_advance_deduction_amount(employee)
        self.police_fine_amount = get_police_fine_deduction_amount(employee)
        self.total_deductions = self.total_statutory_deductions + self.total_non_statutory_deductions
        self.lunch_allowance = int(self.employee.lunch_allowance / self.currency_cost)

    def sum_all_income(self, employee):
        return employee.initial_gross_salary + self.overtime_pay + self.bonus + self.local_service_tax

    @property
    def total_nssf_deduction(self):
        return self.employee_nssf + self.employer_nssf

    @property
    def total_statutory_deductions(self):
        return self.employee_nssf + self.paye + self.local_service_tax_deduction

    @property
    def total_non_statutory_deductions(self):
        return self.sacco_deduction_amount + self.damage_deduction_amount

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions
