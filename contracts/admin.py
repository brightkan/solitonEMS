from django.contrib import admin

# Register your models here.
from contracts.models import Contract, Penalty, Offence, Termination

admin.site.register(Contract)
admin.site.register(Penalty)
admin.site.register(Offence)
admin.site.register(Termination)
