from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_auth.decorators import ems_login_required
from settings.selectors import get_all_currencies, get_currency
from settings.services import update_currency, create_currency


@ems_login_required
def settings_page(request):
    all_currencies = get_all_currencies()
    context = {
        "currencies": all_currencies
    }
    return render(request, 'settings/settings_page.html', context)


def add_currency(request):
    if request.POST:
        code = request.POST.get('code')
        desc = request.POST.get('desc')
        cost = request.POST.get('cost')

        create_currency(code, desc, cost)
        messages.success(request, 'Successfully created currency')

        return HttpResponseRedirect(reverse('settings_page'))
    messages.error(request, 'You sent a get request')
    return HttpResponseRedirect(reverse('settings_page'))


def edit_currency_page(request, currency_id):
    currency = get_currency(currency_id)
    if request.POST:
        code = request.POST.get('code')
        desc = request.POST.get('desc')
        cost = request.POST.get('cost')
        update_currency(currency, code, desc, cost)
        messages.success(request, 'Successfully updated currency')
        return HttpResponseRedirect(reverse('settings_page'))
    context = {
        "currency": currency
    }
    return render(request, 'settings/edit_currency.html', context)


def delete_currency(request, currency_id):
    currency = get_currency(currency_id)
    currency.delete()
    messages.success(request, "Successfully delete currency")
    return HttpResponseRedirect(reverse('settings_page'))
