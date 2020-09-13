from performance.models import DepartmentKPI, EmployeeKPI


def get_all_department_kpi(department):
    return DepartmentKPI.objects.filter(department=department)


def get_all_employee_kpi(employee):
    return EmployeeKPI.objects.filter(employee=employee)


def get_department_kpi(id):
    return DepartmentKPI.objects.get(pk=id)


def get_employee_kpi(id):
    return EmployeeKPI.objects.get(pk=id)

