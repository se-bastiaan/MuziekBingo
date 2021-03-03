from django.conf import settings
from django.core import mail
from django.template import loader

from game.models import Player


def send_welcome_email():
    players = Player.objects.all()

    with mail.get_connection() as connection:
        for player in players:
            email_body = loader.render_to_string(
                "game/emails/welcome.txt",
                {"player": player, "base_url": settings.BASE_URL},
            )

            print(player)

            for email in [player.email1, player.email2]:
                mail.EmailMessage(
                    "Informatie muziekbingo",
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    connection=connection,
                ).send()
