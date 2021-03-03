from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Song, Player, Card


class SongResource(resources.ModelResource):
    class Meta:
        model = Song


@admin.register(Song)
class SongAdmin(ImportExportModelAdmin):
    resource_class = SongResource
    list_display = ("artist", "title", "played")
    search_fields = ("artist", "title")


class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResource
    list_display = ("first_name1", "first_name2", "user_code")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass
