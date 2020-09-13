from django.db import models

# Create your models here.
from employees.models import Employee
from settings.models import Currency


class Department(models.Model):
    name = models.CharField(max_length=45, unique=True)
    hod = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=15, default="Active")

    def __str__(self):
        return self.name


class SalaryScale(models.Model):
    level = models.CharField(max_length=20, null=False, unique=True)
    minimum = models.FloatField()
    maximum = models.FloatField()

    def __str__(self):
        return self.level


class Position(models.Model):
    name = models.CharField(max_length=45, unique=True)
    number_of_slots = models.IntegerField()
    type = models.CharField(max_length=20, default="Full Time")
    salary_scale = models.ForeignKey(SalaryScale, on_delete=models.CASCADE, blank=True, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=15, default="Active")

    def __str__(self):
        return self.name


class OrganisationDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.position.name + " " + self.department.name
