from django.db import models
from django.utils import timezone
from employees.models import Employee
from leave.services import get_number_of_days_without_public_holidays
from organisation_details.models import Team, Department


class Leave_Types(models.Model):
    leave_type = models.CharField(max_length=45)
    leave_days = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.leave_type


class LeaveApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="Employees")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(Leave_Types, on_delete=models.CASCADE)
    apply_date = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField(default=1)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                   related_name="Supervisor", blank=True, null=True)
    supervisor_status = models.CharField(max_length=15, default="Pending")
    supervisor_comment = models.TextField(blank=True, null=True, default="None")
    hod = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="hod", \
                            blank=True, null=True)
    hod_status = models.CharField(max_length=15, default="Pending")
    hod_comment = models.TextField(blank=True, null=True, default="None")
    hr = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="hr", \
                           blank=True, null=True)
    hr_status = models.CharField(max_length=15, default="Pending")
    hr_comment = models.TextField(blank=True, null=True, default="None")
    overall_status = models.CharField(max_length=10, default="Pending")
    remarks = models.TextField(default="None")
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{id} - {self.leave_type} - {employee.first_name}"


class Leave_Records(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_year = models.IntegerField()
    entitlement = models.IntegerField(default=21)
    residue = models.IntegerField(default=0)
    leave_applied = models.IntegerField(default=0)
    total_taken = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)


class annual_planner(models.Model):
    leave_year = models.CharField(max_length=5)
    leave_month = models.CharField(max_length=4, default='Jan')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave_Types, on_delete=models.CASCADE, default=1)
    date_from = models.DateField()
    date_to = models.DateField()
    no_of_days = models.IntegerField(default=0)
    status = models.CharField(max_length=15, default='Pending')


class LeavePlan(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    APPROVAL_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    plan_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    approval_status = models.CharField(
        max_length=8,
        choices=APPROVAL_CHOICES,
        default=PENDING,
    )

    @property
    def no_of_days(self):
        return get_number_of_days_without_public_holidays(self.start_date, self.end_date)
