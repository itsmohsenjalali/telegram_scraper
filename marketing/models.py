from django.db import models
from scraper.models import TelegramGroup
# Create your models here.


class MarketingPlan(models.Model):
    STRATEGY = [
        ('iug', 'Add User'),
        ('smu', 'Send Message To User'),
        ('full', 'Add User and Send Message')
    ]
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    selected_group = models.ManyToManyField(
        TelegramGroup, related_name='marketing_plan')
    strategy = models.CharField(max_length=4, choices=STRATEGY)

    message = models.TextField(blank=True, null=True)
    target_group = models.ForeignKey(
        TelegramGroup,
        on_delete=models.CASCADE,
        limit_choices_to={'is_target': True},
        related_name='plan')

    def __str__(self) -> str:
        return self.title
