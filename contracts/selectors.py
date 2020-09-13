from contracts.models import Contract, Offence, Penalty, Termination
import datetime


def get_contract(contract_id):
    contract = Contract.objects.get(pk=contract_id)
    return contract


def get_penalty(penalty_id):
    penalty = Penalty.objects.get(pk=penalty_id)
    return penalty


def get_termination(termination_id):
    termination = Termination.objects.get(pk=termination_id)
    return termination


def get_offence(offence_id):
    offence = Offence.objects.get(pk=offence_id)
    return offence


def get_all_contracts():
    return Contract.objects.all()


def get_all_offences():
    return Offence.objects.all()


def get_all_penalties():
    return Penalty.objects.all()


def get_active_contracts():
    return Contract.objects.filter(status="Active")


def get_terminated_contracts():
    return Contract.objects.exclude(status="Active")


def get_employee_contracts(employee):
    return Contract.objects.filter(status="Active", employee=employee)


def is_contract_expired(contract):
    """Check if contract is expired"""
    return contract.expiry_date > datetime.date.today()


def get_all_terminations():
    return Termination.objects.all()
