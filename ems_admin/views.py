from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from ems_admin.forms import UserForm, SolitonUserForm, EMSPermissionForm
from ems_admin.selectors import get_bound_user_form, get_user, get_solitonuser, get_bound_soliton_user_form, \
    fetch_all_permissions_or_create, get_permission
from ems_auth.models import SolitonUser

User = get_user_model()


def manage_users_page(request):
    user = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserForm(request.POST)
        soliton_user_form = SolitonUserForm(request.POST)
        # check whether it's valid:
        if user_form.is_valid() and soliton_user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password('solitonug')
            user.save()
            soliton_user = soliton_user_form.save(commit=False)
            soliton_user.user = user
            soliton_user.save()

            return HttpResponseRedirect(reverse(manage_users_page))
        else:

            return HttpResponseRedirect(reverse(manage_users_page))
        # if a GET (or any other method) we'll create a blank form
    else:

        user_form = UserForm()
        soliton_user_form = SolitonUserForm()

        context = {
            "user": user,
            "admin": "active",
            "users": User.objects.all(),
            "user_form": user_form,
            "soliton_user_form": soliton_user_form

        }

        return render(request, 'ems_admin/manage_users.html', context)


def edit_user_page(request, id):
    user = get_user(id)
    user_form = get_bound_user_form(user)

    try:
        soliton_user_form = get_bound_soliton_user_form(user)
    except SolitonUser.DoesNotExist:
        soliton_user_form = SolitonUserForm()

    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        user_form.save()
        soliton_user = get_solitonuser(user)
        try:
            soliton_user_form = SolitonUserForm(request.POST, instance=soliton_user)
            soliton_user_form.save(commit=False)
            soliton_user_form.user = user
            soliton_user_form.save()
            return HttpResponseRedirect(reverse(manage_users_page))
        except ValueError:
            messages.error(request, "The employee can not be assigned to more than one user")
            return HttpResponseRedirect(reverse(manage_users_page))
    else:
        user = request.user
        context = {
            "user": user,
            "admin": "active",
            "user_form": user_form,
            "soliton_user_form": soliton_user_form

        }

        return render(request, 'ems_admin/edit_user.html', context)


def manage_user_permissions_page(request, id):
    user = get_user(id)
    permissions = fetch_all_permissions_or_create(user)

    context = {
        'admin': 'active',
        'permissions': permissions
    }

    return render(request, 'ems_admin/manage_user_permissions.html', context)


def edit_user_permission_page(request, id):
    permission = get_permission(id)
    permission_user = permission.user

    emspermission_form = EMSPermissionForm(instance=permission)

    if request.POST:
        emspermission_form = EMSPermissionForm(request.POST, instance=permission)
        emspermission_form.save()

        return HttpResponseRedirect(reverse(manage_user_permissions_page, args=[permission_user.id]))

    context = {
        'admin': 'active',
        'emspermission_form': emspermission_form,
        'permission': permission,
        'permission_user': permission_user
    }

    return render(request, 'ems_admin/edit_user_permission.html', context)


def view_users_page(request):
    user = request.user
    context = {
        "user": user,
        "admin": "active",
        "users": User.objects.all(),

    }
    return render(request, 'ems_admin/view_users.html', context)