from django.core.management.base import BaseCommand

from apps.pages.utils import (
    update_gold_prices,
    update_silver_prices,
)


class Command(BaseCommand):

    help = "Update gold and silver prices"

    def handle(self, *args, **kwargs):

        update_gold_prices()

        update_silver_prices()

        self.stdout.write(
            self.style.SUCCESS(
                "Gold & Silver prices updated successfully"
            )
        )