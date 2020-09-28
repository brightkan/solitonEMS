from django.contrib import admin

# Register your models here.
from organisation_details.models import Team, Department, Position, OrganisationDetail
from .models import Employee, HomeAddress, Certification, EmergencyContact, Beneficiary, Spouse, Dependant, Deduction, \
    BankDetail, Allowance, StatutoryDeduction

admin.site.site_header = "Soliton Telmec EMS Admin"
admin.site.register(Employee)
admin.site.register(HomeAddress)
admin.site.register(Certification)
admin.site.register(EmergencyContact)
admin.site.register(Beneficiary)
admin.site.register(Spouse)
admin.site.register(Dependant)
admin.site.register(Deduction)
admin.site.register(BankDetail)
admin.site.register(Team)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(OrganisationDetail)
admin.site.register(Allowance)
admin.site.register(StatutoryDeduction)
