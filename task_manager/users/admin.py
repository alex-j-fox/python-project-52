from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'created_at')
    list_filter = ('username', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'first_name', 'last_name')
    prepopulated_fields = {'username': ('username',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
