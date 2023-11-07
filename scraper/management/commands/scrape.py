from django.core.management.base import BaseCommand
from telethon.sync import TelegramClient
from scraper.src import crawl
from scraper.models import TelegramAccount
from django.conf import settings
# from scraper.models import ScraperStatus
# Import your scraping functions or classes here

class Command(BaseCommand):
    help = 'Scrape data and save in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--conversation',
            action='store_true',
            help='Scrape Conversations(Groups and Private Chats)'
        )
        parser.add_argument(
            '--user',
            action='store_true',
            help='Scrape Users in Groups'
        )
        parser.add_argument(
            '--user-message',
            action='store_true',
            help='Scrape Users in SuperGroups With Message'
        )

    def handle(self, *args, **options):
        account = TelegramAccount.objects.filter()
        session_path = settings.BASE_DIR + '/sessions/' + acc.phone_number
        for acc in account:
            client = TelegramClient(session_path, acc.api_id, acc.api_hash)
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(acc.phone_number)
                client.sign_in(acc.phone_number, input('Enter the code: '))
        
            if options['conversation']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Conversations...'))
                crawl.get_conversations(client)
            elif options['user']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Users in Groups...'))
                crawl.get_users_in_group(client)
            elif options['user-message']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Users in SuperGroups With Message...'))
                crawl.get_users_in_group_with_message(client)
        