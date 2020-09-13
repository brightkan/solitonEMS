from django import template

from employees.selectors import get_employee
from performance.procedures import calculate_performance_rating

register = template.Library()


@register.filter
def performance_rating_filter(value: int):
    """Outputs integer with performance score of employee"""
    employee = get_employee(value)
    try:
        return calculate_performance_rating(employee)
    except:
        """Broad Exception hides bad behaviour"""
        return 0


