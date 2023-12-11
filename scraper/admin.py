from django.contrib import admin
from .models import TelegramGroup, TelegramUser, TelegramAccount, ScraperStatus
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Register your models here.

class ScraperStatusAdmin(admin.ModelAdmin):
    list_display = ('job', 'status', 'last_update', 'marketing_plan')
    list_filter = ('job', 'status')


class TelegramGroupAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'participants_count', 'deep_crwal', 'is_super_group')
    list_filter = ('deep_crwal', 'is_super_group', 'is_target')
    sortable_by = ('id', 'title', 'participants_count')

class TelegramUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name')
    filter_horizontal = ('groups',)
    list_filter = ('can_join_groups', 'is_bot', 'is_spam',('groups__title', DropdownFilter))
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
admin.site.register(ScraperStatus, ScraperStatusAdmin)
