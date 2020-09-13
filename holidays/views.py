from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_admin.decorators import log_activity
from ems_auth.decorators import ems_login_required, hr_required
from holidays.models import Holiday
from holidays.selectors import get_all_holidays, get_holiday
from holidays.services import create_holiday


@ems_login_required
@hr_required
@log_activity
def holidays_page(request):
    if request.POST:
        date = request.POST.get('date')
        name = request.POST.get('name')
        holiday = create_holiday(date, name)
        messages.success(request, "Successfully created the holiday")
        return HttpResponseRedirect(reverse('holidays_page'))

    holidays = get_all_holidays()
    context = {
        "holidays_page": "active",
        "holidays": holidays
    }

    return render(request, 'holidays/holidays_page.html', context)


@log_activity
def delete_holiday(request, holiday_id):
    holiday = get_holiday(holiday_id)
    holiday.delete()
    messages.success(request, "Deleted a holiday entry")
    return HttpResponseRedirect(reverse('holidays_page'))


@log_activity
def edit_holiday_page(request, holiday_id):
    holiday = get_holiday(holiday_id)
    if request.POST:
        date = request.POST.get('date')
        name = request.POST.get('name')
        Holiday.objects.filter(id=holiday.id).update(
            name=name,
            date=date
        )
        messages.success(request, "Updated the holiday entry")
        return HttpResponseRedirect(reverse('holidays_page'))
    context = {
        "holidays_page": "active",
        "holiday": holiday
    }
    return render(request, 'holidays/edit_holiday.html', context)
