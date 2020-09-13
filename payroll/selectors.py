from payroll.models import Payslip, PayrollRecord
from settings.selectors import get_ugx_currency, get_usd_currency


def get_payroll_by_id(payroll_id):
    payroll = Payslip.objects.get(pk=payroll_id)
    return payroll


def get_payroll_record_by_id(payroll_record_id):
    payroll_record = PayrollRecord.objects.get(pk=payroll_record_id)
    return payroll_record


def get_ugx_payslips(payroll_record):
    ugx_currency = get_ugx_currency()
    return Payslip.objects.filter(payroll_record=payroll_record, currency=ugx_currency)


def get_unarchived_payroll_records():
    return PayrollRecord.objects.filter(archived=False)


def get_usd_payslips(payroll_record):
    usd_currency = get_usd_currency()
    return Payslip.objects.filter(payroll_record=payroll_record, currency=usd_currency)


def get_payroll_record(id):
    return PayrollRecord.objects.get(pk=id)


def get_payslips(payroll_record):
    return Payslip.objects.filter(payroll_record=payroll_record)
