from django.db import models
from employees.models import Employee
from organisation_details.models import Department


# Create your models here.
class DepartmentKPI(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    measure_of_success = models.TextField()
    weight = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.measure_of_success


class EmployeeKPI(models.Model):
    ASSESSORS = [
        ('HOD', 'Head of Department'),
        ('HR', 'Human Resource Officer'),
        ('Self', 'Self'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    measure_of_success = models.TextField()
    weight = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    assessor = models.CharField(max_length=10, choices=ASSESSORS)

    def __str__(self):
        return self.measure_of_success


