from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'creation_time')
    search_fields = ('name', 'description')
    filter_horizontal = ('members',)