from django.db import models
from employees.models import Employee

# Create your models here.
from settings.models import Currency


class PayrollRecord(models.Model):
    year = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ('year', 'month',)

    def __str__(self):
        return self.month + " " + self.year


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, default="")
    employee_nssf = models.FloatField()
    employer_nssf = models.FloatField()
    gross_salary = models.FloatField()
    net_salary = models.FloatField()
    paye = models.FloatField()
    total_nssf_contrib = models.FloatField(default=0)
    overtime = models.FloatField()
    bonus = models.FloatField(default=0)
    local_service_tax = models.FloatField()
    local_service_tax_deduction = models.FloatField()
    sacco_deduction = models.FloatField()
    damage_deduction = models.FloatField()
    salary_advance = models.FloatField()
    police_fine = models.FloatField()
    prorate = models.CharField(max_length=20, default="0.0")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default="")
    basic_salary = models.IntegerField(default=0)
    currency_rate = models.IntegerField(default=0)

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name

    @property
    def total_statutory(self):
        return self.total_nssf_contrib + self.paye + self.local_service_tax_deduction

    @property
    def paye_ugx(self):
        paye = self.paye
        currency = float(self.currency.cost)
        return paye * currency

    @property
    def nssf_ugx(self):
        nssf = self.total_nssf_contrib
        currency = float(self.currency.cost)
        return nssf * currency
