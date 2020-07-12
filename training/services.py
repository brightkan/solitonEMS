from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from overtime.selectors import get_hr_users, get_hod_users, get_cfo_users, get_ceo_users
from overtime.services import send_overtime_application_mail
from training.models import Training


def approve_overtime_application_finally(id):
    # Get the training application
    training_application = Training.objects.get(pk=id)
    training_application.status = "Approved"
    training_application.save()
    return training_application


def reject_finally(training_application):
    training_application.status = "Rejected"
    training_application.save()
    return training_application


def supervisor_reject(training_application):
    training_application.supervisor_approval = "Rejected"
    training_application.save()
    return training_application


def supervisor_approve(training_application):
    training_application.supervisor_approval = "Approved"
    training_application.save()
    approvers = get_hod_users(training_application.applicant)
    send_training_application_mail(approvers, training_application)
    return training_application


def hr_approve(training_application):
    training_application.HR_approval = "Approved"
    training_application.save()
    approvers = get_cfo_users()
    send_training_application_mail(approvers, training_application)
    return training_application


def hr_reject(overtime_application):
    overtime_application.HR_approval = "Rejected"
    overtime_application.save()
    return overtime_application


def hod_reject(training_application):
    training_application.HOD_approval = 'Rejected'
    training_application.save()
    return training_application


def cfo_reject(training_application):
    training_application.cfo_approval = 'Rejected'
    training_application.save()
    return training_application


def ceo_reject(training_application):
    training_application.ceo_approval = 'Rejected'
    training_application.save()
    return training_application


def hod_approve(training_application):
    # Get the training application
    training_application.HOD_approval = 'Approved'
    training_application.save()
    approvers = get_hr_users()
    send_training_application_mail(approvers, training_application)
    return training_application


def cfo_approve(training_application):
    training_application.cfo_approval = 'Approved'
    training_application.save()
    approvers = get_ceo_users()
    send_training_application_mail(approvers, training_application)
    return training_application


def ceo_approve(training_application):
    # Get the training application
    training_application.ceo_approval = 'Approved'
    training_application.status = "Approved"
    training_application.save()
    return training_application


def approve_training_application_service(approver, training_application):
    approved_training_application = None

    if approver.is_supervisor:
        approved_training_application = supervisor_approve(training_application)

    if approver.is_hod:
        approved_training_application = hod_approve(training_application)

    if approver.is_hr:
        approved_training_application = hr_approve(training_application)

    if approver.is_cfo:
        approved_training_application = cfo_approve(training_application)

    if approver.is_ceo:
        approved_training_application = ceo_approve(training_application)
        send_training_application_approval_mail(training_application)

    return approved_training_application


def reject_training_application_service(rejecter, training_application):
    if rejecter.is_supervisor:
        rejected_training_application = supervisor_reject(training_application)

    elif rejecter.is_hod:
        rejected_training_application = hod_reject(training_application)

    elif rejecter.is_hr:
        rejected_training_application = hr_reject(training_application)

    elif rejecter.is_cfo:
        rejected_training_application = cfo_reject(training_application)

    elif rejecter.is_ceo:
        rejected_training_application = ceo_reject(training_application)
    else:
        rejected_training_application = None

    return rejected_training_application


def send_training_application_mail(approvers, training_application, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        "applicant_name": training_application.applicant,
        "server_url": domain
    }

    subject, from_email, to = 'New Training Applications', None, approver_emails,
    html_content = get_template("email/training_approval_notification.html").render(context)
    msg = EmailMultiAlternatives(subject, None, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_training_application_approval_mail(training_application, domain=None):
    applicant = training_application.applicant
    user = applicant.solitonuser.user

    context = {
        "applicant": applicant,
        "training_application": training_application,
        "server_url": domain
    }

    subject, from_email, to = 'Training Application Approval', None, user,
    html_content = get_template("email/training_approved_notification.html").render(context)
    msg = EmailMultiAlternatives(subject, None, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
