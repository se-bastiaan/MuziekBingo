# Generated by Django 3.1.7 on 2021-03-03 19:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name1", models.CharField(max_length=250)),
                ("last_name1", models.CharField(max_length=250)),
                ("first_name2", models.CharField(max_length=250)),
                ("last_name2", models.CharField(max_length=250)),
                ("email1", models.EmailField(max_length=254)),
                ("email2", models.EmailField(max_length=254)),
                ("code", models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("artist", models.CharField(max_length=250)),
                ("played", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "item11",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item12",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item13",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item14",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item15",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item21",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item22",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item23",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item24",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item25",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item31",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item32",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item33",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item34",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item35",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item41",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item42",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item43",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item44",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item45",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item51",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item52",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item53",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item54",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "item55",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.song",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.player"
                    ),
                ),
            ],
        ),
    ]
