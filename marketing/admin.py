from django.contrib import admin
from .models import MarketingPlan
# Register your models here.


class MarketingPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'strategy')
    filter_horizontal = ('selected_group',)
    fieldsets = (
        ('Marketing Plan Info', {
            'fields': ('title', 'start_date', 'strategy', 'target_group' ,'message')
        }),
        ('Selected Groups', {
            'fields': ('selected_group',)
        })
    )

admin.site.register(MarketingPlan, MarketingPlanAdmin)