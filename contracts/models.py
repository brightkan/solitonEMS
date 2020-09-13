from django.db import models

# Create your models here.
from employees.models import Employee
from organisation_details.models import Position


class Contract(models.Model):
    reference_number = models.IntegerField(unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=40)
    effective_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, default="Active")
    risk = models.CharField(max_length=10)
    document = models.FileField(upload_to="contracts")

    def __str__(self):
        return "Contract {}".format(str(self.reference_number))


class Penalty(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class Offence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    resolved = models.CharField(max_length=30)
    penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Termination(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    termination_letter = models.FileField(upload_to="termination_letters", blank=True)
    clearance_form = models.FileField(upload_to="termination_forms", blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField()

    def __str(self):
        return self.employee
