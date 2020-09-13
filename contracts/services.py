from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from contracts.selectors import is_contract_expired
from employees.services import suspend
from notification.services import send_hr_notification_on_contract_expiry, send_employee_notification_on_contract_expiry

User = get_user_model()


def terminate(contract):
    employee = contract.employee
    suspend(employee)
    contract.status = "Passive"
    contract.save()
    return contract


def activate(contract):
    employee = contract.employee
    employee.status = "Active"
    employee.save()
    contract.status = "Active"
    contract.save()
    return contract


def send_hr_mail_on_contract_expiry(approvers, contract, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        "applicant_name": contract.applicant,
        "server_url": domain
    }

    subject, from_email, to = 'Contract Expiry', None, approver_emails,
    html_content = get_template("email/hr_contract_expiry_reminder.html").render(context)
    msg = EmailMultiAlternatives(subject, None, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_reminder_on_contract_expiry(contract):
    """Send notification alerts to employee and HR"""
    hr_users = User.objects.filter(is_hr=True)
    if is_contract_expired(contract):
        send_hr_notification_on_contract_expiry(hr_users, contract)
        send_employee_notification_on_contract_expiry(contract)
    else:
        pass
