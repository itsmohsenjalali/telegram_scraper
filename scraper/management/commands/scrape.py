from django.core.management.base import BaseCommand
from telethon.sync import TelegramClient
from scraper.src import crawl
from scraper.models import TelegramAccount
from marketing.models import MarketingPlan
from django.conf import settings
from telethon.sessions import StringSession
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
            '--user_message',
            action='store_true',
            help='Scrape Users in SuperGroups With Message'
        )
        parser.add_argument(
            '--check_deep_crawl',
            action='store_true',
            help='Check Deep Crawl Groups'
        )
        parser.add_argument(
            '--clean_db',
            action='store_true',
            help='Clean Database'
        )
        parser.add_argument(
            '--clean_channel',
            action='store_true',
            help='Clean Channel'
        )
        parser.add_argument(
            '--invite_user_to_group',
            action='store_true',
            help='Invite User To Group'
        )

    def handle(self, *args, **options):
        account = TelegramAccount.objects.filter()
        marketing_plan = MarketingPlan.objects.first()
        for acc in account:
            client = TelegramClient(StringSession(acc.session), acc.api_id, acc.api_hash)
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(acc.phone_number)
                client.sign_in(acc.phone_number, input('Enter the code: '))
                acc.session = StringSession.save(client.session)
                acc.save()

            if options['conversation']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Conversations...'))
                crawl.get_conversations(client)
            elif options['user']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Users in Groups...'))
                crawl.get_users_in_group(client)
            elif options['user_message']:
                self.stdout.write(self.style.SUCCESS('Start Scraping Users in SuperGroups With Message...'))
                crawl.get_users_in_group_with_message(client)
            elif options['clean_db']:
                self.stdout.write(self.style.SUCCESS('Start Cleaning Database Zero Member Group And Fake User...'))
                crawl.clean_db()
            elif options['clean_channel']:
                self.stdout.write(self.style.SUCCESS('Start Cleaning Channel...'))
                crawl.clean_channel(client)
            elif options['invite_user_to_group']:
                self.stdout.write(self.style.SUCCESS('Start Inviting Users To Group...'))
                crawl.invite_users_to_channel(client, marketing_plan)
