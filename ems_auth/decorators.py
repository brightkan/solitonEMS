from django.contrib.auth import logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from ems_admin.selectors import get_user
from ems_auth.models import SolitonUser


User = get_user_model()


def ems_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('login'))

    return wrapper



def super_admin_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('super_admin_required_page'))

    return wrapper


def employee_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        try:
            solitonuser = user.solitonuser
            return function(request, *args, **kw)
        except SolitonUser.DoesNotExist:
            return render(request, "employee_required.html")

    return wrapper


def hr_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_hr:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('hr_required_page'))

    return wrapper


def hod_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_hod:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('hod_required_page'))

    return wrapper


def first_login(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.password_changed:
            user.password_changed = True
            user.save()
            logout(request)
            return render(request, "ems_auth/first_time_login.html")
        else:
            return function(request, *args, **kwargs)

    return wrapper


def employees_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Employees")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def organisation_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Organisation")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def leave_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         ems_permission = EMSPermission.objects.filter(user=user, name="Leave")[0]
    #         if ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def payroll_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Payroll")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def overtime_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Overtime")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def holidays_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Holidays")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def recruitment_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Recruitment")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def contracts_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Contracts")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except:
    #         return function(request, **kw)
    # return wrapper
    pass


def training_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Training")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass


def learning_and_development_full_auth_required(function):
    # def wrapper(request, **kw):
    #     try:
    #         user_id = request.user.id
    #         user = get_user(user_id)
    #         try:
    #             ems_permission = EMSPermission.objects.filter(user=user, name="Learning and Development")[0]
    #         except IndexError:
    #             ems_permission = None
    #
    #         if ems_permission and ems_permission.full_auth:
    #             return function(request, **kw)
    #         else:
    #             return render(request, "ems_auth/full_auth_required.html")
    #
    #     except User.DoesNotExist:
    #         return function(request, **kw)
    #
    # return wrapper
    pass
