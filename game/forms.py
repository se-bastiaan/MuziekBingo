from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from game.models import Card, Player


class LoginForm(forms.Form):
    user_code = forms.CharField(
        label="Code", max_length=7, validators=[RegexValidator("^[A-z]{3}-[A-z]{3}$")]
    )

    def clean(self):
        cleaned_data = super().clean()
        user_code = cleaned_data.get("user_code")

        if user_code:
            player = Player.objects.filter(
                code=user_code.replace("-", "").upper()
            ).first()
            if not player:
                raise ValidationError("We konden geen speler vinden voor deze code.")
