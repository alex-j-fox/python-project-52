from django.contrib import admin

from task_manager.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'date_joined',
        'is_staff',
        'is_active')
    list_display_links = ('id', 'username')
    list_filter = ('username', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name')
    prepopulated_fields = {'username': ('username',)}
    date_hierarchy = 'date_joined'
    ordering = ('-date_joined',)
