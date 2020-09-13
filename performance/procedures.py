from django.db.models import Sum

from performance.selectors import get_all_department_kpi, get_all_employee_kpi


def get_total_score(kpis):
    sum = kpis.aggregate(Sum('score'))
    total_score = sum['score__sum']
    return total_score


def get_total_weight(kpis):
    sum = kpis.aggregate(Sum('weight'))
    total_score = sum['weight__sum']
    return total_score


def calculate_performance_rating(employee) -> int:
    department = employee.organisationdetail.department
    department_kpis = get_all_department_kpi(department)
    employee_kpis = get_all_employee_kpi(employee=employee)
    department_total_score = get_total_score(department_kpis)
    department_total_weight = get_total_weight(department_kpis)
    employee_total_score = get_total_score(employee_kpis)
    employee_total_weight = get_total_weight(employee_kpis)

    try:
        total_score = employee_total_score + department_total_score
        total_weight = employee_total_weight + department_total_weight

        performance_rating = (total_score / total_weight) * 100
    except (ZeroDivisionError, TypeError):
        performance_rating = 0
    return int(performance_rating)  # Round off to the nearest integer
