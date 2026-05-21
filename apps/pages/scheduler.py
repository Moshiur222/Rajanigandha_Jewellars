from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
import logging

from .utils import (
    update_gold_prices,
    update_silver_prices,
)

logger = logging.getLogger(__name__)


def start():

    scheduler = BackgroundScheduler()

    scheduler.add_jobstore(
        DjangoJobStore(),
        "default"
    )

    # GOLD PRICE UPDATE
    scheduler.add_job(
        update_gold_prices,
        trigger="interval",
        hours=1,
        id="gold_price_job",
        replace_existing=True,
    )

    # SILVER PRICE UPDATE
    scheduler.add_job(
        update_silver_prices,
        trigger="interval",
        hours=1,
        id="silver_price_job",
        replace_existing=True,
    )

    try:
        scheduler.start()
        logger.info("Scheduler started...")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")