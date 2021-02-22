from django.shortcuts import render
import random

from django.http import Http404

from django.views.generic import FormView, DetailView
from django.shortcuts import redirect
from game.forms import LoginForm
from game.models import Card, Player, Song


class LoginView(FormView):
    template_name = "game/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user_code = form.cleaned_data["user_code"].replace('-', '').upper()
        player = Player.objects.filter(code=user_code).first()


        if player.card_set.count() == 0:
            song_pks = Song.objects.values_list('pk', flat=True)
            selected_pks = random.sample(list(song_pks), 25)
            songs = Song.objects.filter(pk__in=selected_pks)

            new_card = Card()
            new_card.player = player
            new_card.items = songs
            new_card.save()

        return redirect("game:card", pk=player.card_set.first().pk)


class CardView(DetailView):
    model = Card
