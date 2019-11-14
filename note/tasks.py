from celery.decorators import task
from celery.utils.log import get_task_logger

from .Lib.test import send_reminder_mail

logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_feedback_email_task(subject, message, sender, reciever):
    """sends an email when feedback form is filled successfully"""
    logger.info("Reminder email")
    return send_reminder_mail(subject, message, sender, reciever)