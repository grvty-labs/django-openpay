from django.db.models import Q

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime

from . import models, hardcode

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(hour=23, minute=59)),
    name="updateSubscriptions",
    ignore_result=True
)
def updateSubscriptions():
    logger.info("Updating Subscriptions information from Openpay's servers...")

    subscriptions_in_system = models.Subscription.objects.filter(
        Q(charge_date__gte=datetime.now().date()) | Q(charge_date=None)
    ).exclude(
        status=hardcode.subscription_status_cancelled)

    if subscriptions_in_system.exists():
        for subscription in subscriptions_in_system.iterator():
            subscription.op_refresh(save=True)

    logger.info("System subscriptions up to date with Openpay's servers.")
