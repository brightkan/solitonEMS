from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from contracts.models import Contract, Penalty, Offence, Termination
from contracts.selectors import get_contract, get_terminated_contracts, get_active_contracts, get_employee_contracts, \
    get_all_offences, get_all_penalties, get_penalty, get_offence, get_all_terminations, get_termination
from contracts.services import activate, terminate
from employees.procedures import send_notification
from employees.selectors import get_employee, get_active_employees
from ems_admin.decorators import log_activity
from ems_auth.decorators import hr_required
from notification.services import send_notification_generic
from organisation_details.selectors import get_position, get_all_positions


@hr_required
@log_activity
def manage_job_contracts(request):
    if request.POST and request.FILES:
        reference_number = request.POST.get('reference_number')
        position_id = request.POST.get('position')
        employee_id = request.POST.get('employee')
        effective_date = request.POST.get('effective_date')
        expiry_date = request.POST.get('expiry_date')
        risk = request.POST.get('risk')
        contract_type = request.POST.get('contract_type')
        document = request.FILES.get('document')

        position = get_position(position_id)
        employee = get_employee(employee_id)
        try:
            new_contract = Contract.objects.create(
                reference_number=reference_number,
                position=position,
                employee=employee,
                effective_date=effective_date,
                expiry_date=expiry_date,
                risk=risk,
                type=contract_type,
                document=document
            )
        except IntegrityError:
            messages.warning(request, "The reference number needs to be unique")

        return HttpResponseRedirect(reverse(manage_job_contracts))

    positions = get_all_positions()
    employees = get_active_employees()
    contracts = get_active_contracts()
    context = {
        "contracts_page": "active",
        "employees": employees,
        "positions": positions,
        "contracts": contracts,
    }
    return render(request, 'contracts/manage_job_contracts.html', context)


@log_activity
def terminate_contract(request, contract_id):
    contract = get_contract(contract_id)
    terminate(contract)
    return HttpResponseRedirect(reverse(manage_job_contracts))


@hr_required
@log_activity
def edit_contract_page(request, contract_id):
    if request.POST and request.FILES:
        reference_number = request.POST.get('reference_number')
        position_id = request.POST.get('position')
        employee_id = request.POST.get('employee')
        effective_date = request.POST.get('effective_date')
        expiry_date = request.POST.get('expiry_date')
        risk = request.POST.get('risk')
        document = request.FILES.get('document')

        position = get_position(position_id)
        employee = get_employee(employee_id)

        contract_list = Contract.objects.filter(id=contract_id)
        contract_list.update(
            reference_number=reference_number,
            position=position,
            employee=employee,
            effective_date=effective_date,
            expiry_date=expiry_date,
            risk=risk,
            document=document
        )

        return HttpResponseRedirect(reverse(manage_job_contracts))

    contract = get_contract(contract_id)
    positions = get_all_positions()
    employees = get_active_employees()
    context = {
        "contracts_page": "active",
        "contract": contract,
        "employees": employees,
        "positions": positions,
    }
    return render(request, 'contracts/edit_contract.html', context)


@log_activity
def terminated_contracts_page(request):
    terminated_contracts = get_terminated_contracts()
    context = {
        "contracts_page": "active",
        "terminated_contracts": terminated_contracts
    }

    return render(request, 'contracts/terminated_contracts.html', context)


@hr_required
@log_activity
def activate_contract(request, contract_id):
    contract = get_contract(contract_id)
    activate(contract)

    return HttpResponseRedirect(reverse(manage_job_contracts))


@hr_required
@log_activity
def user_contracts_page(request):
    user = request.user
    employee = user.solitonuser.employee

    contracts = get_employee_contracts(employee)
    context = {
        "contracts_page": "active",
        "contracts": contracts,
    }

    return render(request, 'contracts/user_contracts.html', context)


@hr_required
@log_activity
def manage_offences_page(request):
    if request.POST:
        name = request.POST.get('name')
        employee_id = request.POST.get('employee')
        penalty_id = request.POST.get('penalty')
        resolved = request.POST.get('resolved')
        description = request.POST.get('description')
        penalty = get_penalty(penalty_id)
        employee = get_employee(employee_id)
        try:
            new_offence = Offence.objects.create(
                name=name,
                penalty=penalty,
                employee=employee,
                resolved=resolved,
                description=description
            )

            send_notification_generic(employee, "Offence Recorded", "You have a new offence recorded")
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add a new offence")

        return HttpResponseRedirect(reverse(manage_offences_page))

    offences = get_all_offences()
    employees = get_active_employees()
    penalties = get_all_penalties()
    context = {
        "contracts_page": "active",
        "employees": employees,
        "offences": offences,
        "penalties": penalties
    }
    return render(request, 'contracts/manage_offences.html', context)


@hr_required
@log_activity
def edit_offence_page(request, offence_id):
    if request.POST:
        name = request.POST.get('name')
        employee_id = request.POST.get('employee')
        penalty_id = request.POST.get('penalty')
        resolved = request.POST.get('resolved')
        description = request.POST.get('description')
        penalty = get_penalty(penalty_id)
        employee = get_employee(employee_id)

        offence_list = Offence.objects.filter(id=offence_id)
        offence_list.update(
            name=name,
            penalty=penalty,
            employee=employee,
            resolved=resolved,
            description=description
        )

        return HttpResponseRedirect(reverse(manage_offences_page))

    offence = get_offence(offence_id)
    offences = get_all_offences()
    employees = get_active_employees()
    penalties = get_all_penalties()
    context = {
        "contracts_page": "active",
        "employees": employees,
        "offences": offences,
        "penalties": penalties,
        "offence": offence
    }
    return render(request, 'contracts/edit_offence.html', context)


@hr_required
@log_activity
def delete_offence(request, offence_id):
    offence = get_offence(offence_id)
    offence.delete()
    return HttpResponseRedirect(reverse(manage_offences_page))


@hr_required
@log_activity
def manage_penalties_page(request):
    if request.POST:
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            new_penalty = Penalty.objects.create(
                name=name,
                description=description
            )

        except IntegrityError:
            messages.warning(request, "There integrity problems while adding new penalty")

        return HttpResponseRedirect(reverse(manage_penalties_page))

    penalties = get_all_penalties()
    context = {
        "contracts_page": "active",
        "penalties": penalties,
    }
    return render(request, 'contracts/manage_penalties.html', context)


@hr_required
@log_activity
def edit_penalty_page(request, penalty_id):
    if request.POST:
        name = request.POST.get('name')
        description = request.POST.get('description')
        penalty_list = Penalty.objects.filter(id=penalty_id)
        penalty_list.update(
            name=name,
            description=description
        )
        return HttpResponseRedirect(reverse(manage_penalties_page))

    penalty = get_penalty(penalty_id)
    context = {
        "contracts_page": "active",
        "penalty": penalty
    }
    return render(request, 'contracts/edit_penalty.html', context)


@hr_required
@log_activity
def delete_penalty(request, penalty_id):
    penalty = get_penalty(penalty_id)
    penalty.delete()
    return HttpResponseRedirect(reverse(manage_penalties_page))


@hr_required
@log_activity
def manage_terminations_page(request):
    if request.POST:
        employee_id = request.POST.get('employee')
        type = request.POST.get('type')
        termination_letter = request.FILES.get('termination_letter')
        clearance_form = request.FILES.get('clearance_form')
        description = request.POST.get('description')
        employee = get_employee(employee_id)

        try:
            new_termination = Termination.objects.create(
                employee=employee,
                type=type,
                termination_letter=termination_letter,
                clearance_form=clearance_form,
                description=description
            )
            send_notification_generic(employee, "Termination Recorded", "Your termination record has been created")
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add a new offence")

        return HttpResponseRedirect(reverse(manage_terminations_page))

    terminations = get_all_terminations()
    employees = get_active_employees()
    context = {
        "contracts_page": "active",
        "employees": employees,
        "terminations": terminations,
    }
    return render(request, 'contracts/manage_terminations.html', context)


@hr_required
@log_activity
def edit_termination_page(request, termination_id):
    if request.POST and request.FILES:
        employee_id = request.POST.get('employee')
        type = request.POST.get('type')
        termination_letter = request.FILES.get('termination_letter')
        clearance_form = request.FILES.get('clearance_form')
        description = request.POST.get('description')
        employee = get_employee(employee_id)
        termination_list = Termination.objects.filter(id=termination_id)

        try:
            termination_list.update(
                employee=employee,
                type=type,
                termination_letter=termination_letter,
                clearance_form=clearance_form,
                description=description
            )
            return HttpResponseRedirect(reverse(manage_terminations_page))
        except IntegrityError:
            messages.warning(request, "Integrity problems with trying to add a new offence")

    termination = get_termination(termination_id)
    terminations = get_all_terminations()
    employees = get_active_employees()
    context = {
        "contracts_page": "active",
        "termination": termination,
        "terminations": terminations,
        "employees": employees
    }
    return render(request, 'contracts/edit_termination.html', context)


@hr_required
@log_activity
def delete_termination(request, termination_id):
    termination = get_termination(termination_id)
    termination.delete()
    return HttpResponseRedirect(reverse(manage_terminations_page))
