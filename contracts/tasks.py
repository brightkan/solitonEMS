from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from contracts.models import Contract
from contracts.services import send_reminder_on_contract_expiry

logger = get_task_logger(__name__)


def send_reminders_for_all_expired_contracts():
    contracts = Contract.objects.filter(status="Active")
    for contract in contracts:
        send_reminder_on_contract_expiry(contract)
    return True


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_send_contract_exipiry_alert()",
    ignore_result=True
)
def task_send_contract_exipiry_alert():
    """
    Sends contract expiry alert every day
    """
    send_reminders_for_all_expired_contracts()
    logger.info("Sent contract expiry alert")
