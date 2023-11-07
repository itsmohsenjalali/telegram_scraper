from django.db import models

# Create your models here.

class TelegramAccount(models.Model):
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.phone_number
    
class TelegramGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    is_super_group = models.BooleanField(default=False)
    participants_count = models.IntegerField(default=0)
    deep_crwal = models.BooleanField(default=False)
    telegram_account = models.ManyToManyField(TelegramAccount, related_name='groups', blank=True)

    def __str__(self) -> str:
        return self.title

class TelegramUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    can_join_groups = models.BooleanField(default=True)
    groups = models.ManyToManyField(TelegramGroup, related_name='members', blank=True)
