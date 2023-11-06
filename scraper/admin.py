from django.contrib import admin
from .models import TelegramGroup, TelegramUser, TelegramAccount
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Register your models here.

class TelegramGroupAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'participants_count')
    sortable_by = ('id', 'title', 'participants_count')

class TelegramUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name')
    filter_horizontal = ('groups',)
    list_filter = ('can_join_groups',('groups__title', DropdownFilter))
    list_display = ('id', 'username', 'first_name', 'last_name', 'can_join_groups')
    fieldsets = (
        ('User Info', {
            'fields': ('id', 'username', 'first_name', 'last_name', 'phone_number', 'can_join_groups')
        }),
        ('Groups', {
            'fields': ('groups',)
        })
    )
    


admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(TelegramAccount)
admin.site.register(TelegramUser, TelegramUserAdmin)
