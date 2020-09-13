from django.contrib import admin

# Register your models here.
from .models import Leave_Types, LeaveApplication, Leave_Records, LeavePlan

admin.site.register(Leave_Types)
admin.site.register(LeaveApplication)
admin.site.register(Leave_Records)
admin.site.register(LeavePlan)