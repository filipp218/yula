from django.contrib import admin
from players.models import Player, Team, Comment
# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name","lastname")}

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Comment)
