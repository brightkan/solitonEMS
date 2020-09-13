from django.contrib import admin

# Register your models here.
from ems_admin.models import  AuditTrail


admin.site.register(AuditTrail)