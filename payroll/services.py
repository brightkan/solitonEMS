from employees.models import Employee
from employees.selectors import get_active_employees
from payroll.simple_payslip import SimplePayslip
from payroll.models import Payslip
from payroll.procedures import get_overtime_pay


def create_payslip_list_service(payroll_record):
    payslips = []
    employees = get_active_employees()

    for employee in employees:
        bonus = employee.bonus
        overtime_pay = get_overtime_pay(employee)
        payslip = create_payslip_service(employee, payroll_record, bonus=bonus, overtime_pay=overtime_pay)
        payslips.append(payslip)

    return payslips


def create_payslip_service(employee: object, payroll_record: object, overtime_pay: object = None,
                           bonus: object = None) -> object:
    simple_payslip = SimplePayslip(employee, overtime_pay=overtime_pay, bonus=bonus)
    payslip = Payslip.objects.create(
        employee=employee,
        payroll_record=payroll_record,
        employee_nssf=simple_payslip.employee_nssf,
        employer_nssf=simple_payslip.employer_nssf,
        gross_salary=simple_payslip.gross_salary,
        net_salary=simple_payslip.net_salary,
        paye=simple_payslip.paye,
        total_nssf_contrib=simple_payslip.total_nssf_deduction,
        overtime=simple_payslip.overtime_pay,
        bonus=simple_payslip.bonus,
        local_service_tax=simple_payslip.local_service_tax,
        local_service_tax_deduction=simple_payslip.local_service_tax_deduction,
        sacco_deduction=simple_payslip.sacco_deduction_amount,
        damage_deduction=simple_payslip.damage_deduction_amount,
        salary_advance=simple_payslip.salary_advance_amount,
        police_fine=simple_payslip.police_fine_amount,
        currency=employee.currency,
        basic_salary=employee.basic_salary,
    )

    return payslip
