import datetime

from .models import Notification
from ems_admin.models import User


def create_notification(title, message, receivers):
    for receiver in receivers:
        user = User.objects.get(pk=receiver.id)

        notification = Notification.objects.create(
            title=title,
            message=message,
            date_time=datetime.datetime.now(),
            user=user
        )


def send_hr_notification_on_contract_expiry(hr_users, contract):
    message = "{} contract has expired. Terminate/Extend".format(contract.employee)
    create_notification(
        "Contract Expiry",
        message,
        hr_users
    )
    return True


def send_employee_notification_on_contract_expiry(contract):
    message = "Your contract has expired"
    employee_user = contract.employee.solitonuser.user
    create_notification(
        "Contract Expiry",
        message,
        [employee_user]
    )
    return True


def send_notification_generic(employee, title, message):
    employee_user = employee.solitonuser.user

    # Send alert
    create_notification(
        title,
        message,
        [employee_user]
    )

    return True
