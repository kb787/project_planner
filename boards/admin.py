from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Board, Task

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'status', 'creation_time')
    list_filter = ('status', 'team')
    search_fields = ('name', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'user', 'status', 'creation_time')
    list_filter = ('status', 'board')
    search_fields = ('title', 'description')