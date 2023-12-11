from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TelegramAccount
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from .utilise import COMMON_JOB

from scraper.models import ScraperStatus

@receiver(post_save, sender=ScraperStatus)
def start_scraping(sender, instance, created, **kwargs):
    if created:
        account = TelegramAccount.objects.first()
        client = TelegramClient(StringSession(account.session), account.api_id, account.api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(account.phone_number)
            client.sign_in(account.phone_number, input('Enter the code: '))
            account.session = StringSession.save(client.session)
            account.save()
        print('Start Scraping')
        COMMON_JOB[instance.job](client,instance.marketing_plan)
        print('Done Scraping')
        instance.status = 'Completed'
        instance.save()

