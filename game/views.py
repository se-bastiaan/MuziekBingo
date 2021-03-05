from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
import random

from django.http import Http404
from django.utils.decorators import method_decorator

from django.views.generic import FormView, DetailView
from django.shortcuts import redirect
from game.forms import LoginForm
from game.models import Card, Player, Song


class LoginView(FormView):
    template_name = "game/login.html"
    form_class = LoginForm

    def _create_card(self, player):
        try:
            song_pks = Song.objects.values_list("pk", flat=True)

            selected_pks = (
                random.sample(list(song_pks)[:16], 5)
                + random.sample(list(song_pks)[16:32], 5)
                + random.sample(list(song_pks)[32:48], 5)
                + random.sample(list(song_pks)[48:64], 5)
                + random.sample(list(song_pks)[64:], 5)
            )
            songs = Song.objects.filter(pk__in=selected_pks)

            new_card = Card()
            new_card.player = player
            new_card.items = songs
            new_card.full_clean()
            new_card.save()
            return False
        except:
            return True

    def form_valid(self, form):
        user_code = form.cleaned_data["user_code"].replace("-", "").upper()
        player = Player.objects.filter(code=user_code).first()

        if player.card_set.count() == 0:
            song_pks = Song.objects.values_list("pk", flat=True)

            if len(song_pks) == 0:
                messages.error(
                    self.request, "De bingokaarten zijn nog niet beschikbaar."
                )
                return redirect("game:login")

            while self._create_card(player):
                print("Have to retry")

        return redirect("game:card", pk=player.card_set.first().pk)


class CardView(DetailView):
    model = Card


@method_decorator(staff_member_required, name="dispatch")
class AdminCardView(DetailView):
    model = Card
    template_name = 'game/card_admin.html'
