from apscheduler.schedulers.background import BackgroundScheduler

from .utils import (
    update_gold_prices,
    update_silver_prices,
)


def start():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        update_gold_prices,
        "interval",
        hours=24,
    )

    scheduler.add_job(
        update_silver_prices,
        "interval",
        hours=24,
    )

    scheduler.start()