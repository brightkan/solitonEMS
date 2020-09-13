from django.contrib import admin

from performance.models import DepartmentKPI, EmployeeKPI

admin.site.register(DepartmentKPI)
admin.site.register(EmployeeKPI)
