from django.db import models

# Create your models here.


class TelegramAccount(models.Model):
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    session = models.TextField(null=True, blank=True)

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
    telegram_account = models.ManyToManyField(
        TelegramAccount, related_name='groups', blank=True)
    is_target = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class TelegramUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    can_join_groups = models.BooleanField(default=True)
    is_bot = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        TelegramGroup, related_name='members', blank=True)


class ScraperStatus(models.Model):
    JOBS = [
        ('sc', 'Scrape Conversations'),
        ('sug', 'Scrape Users in Groups'),
        ('sugm', 'Scrape Users in SuperGroups With Message'),
        ('iuc', 'Invite Users To Channel'),
        ('iug', 'Invite User To Group'),
        ('smu', 'Send Message To User'),
    ]
    STATUS = [
        ('r', 'Running'),
        ('p', 'Puaused'),
        ('c', 'Completed'),
    ]
    last_group_visited = models.BigIntegerField(null=True, blank=True)
    last_user_visited = models.BigIntegerField(null=True, blank=True)
    last_message_visited = models.BigIntegerField(null=True, blank=True)
    job = models.CharField(max_length=10, choices=JOBS)
    interval = models.IntegerField(default=144)
    status = models.CharField(max_length=1, choices=STATUS)
    last_update = models.DateTimeField(auto_now=True)

    marketing_plan = models.ForeignKey(
        'marketing.MarketingPlan', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.status