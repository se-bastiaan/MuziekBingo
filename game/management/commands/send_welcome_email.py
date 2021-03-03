from django.core.management.base import BaseCommand

from game import emails


class Command(BaseCommand):
    def handle(self, *args, **options):
        emails.send_welcome_email()
