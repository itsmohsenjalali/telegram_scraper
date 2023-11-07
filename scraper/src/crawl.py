from telethon.sync import TelegramClient
from telethon.functions import channels
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.types import Chat, User, Channel
from scraper.models import TelegramGroup, TelegramAccount, TelegramUser
from alive_progress import alive_bar
import time


def get_conversations(client: TelegramClient):
    conversations = client.iter_dialogs()
    telegram_account = TelegramAccount.objects.get(
        phone_number=client.get_me().phone)
    with alive_bar() as bar:
        for conversation in conversations:
            try:
                if isinstance(conversation.entity, Channel) or isinstance(conversation.entity, Chat):
                    if hasattr(conversation.entity, 'megagroup') and hasattr(conversation.entity, 'broadcast'):
                        if conversation.entity.gigagroup == True:
                            continue
                        if conversation.entity.broadcast == True:
                            continue
                        is_super_group = True
                        if hasattr(conversation.entity, 'default_banned_rights'):
                            if hasattr(conversation.entity.default_banned_rights, 'send_messages'):
                                if conversation.entity.default_banned_rights.send_messages == True:
                                    is_super_group = False
                        TelegramGroup.objects.update_or_create(
                            id=conversation.id,
                            defaults={
                                'title': conversation.title,
                                'is_super_group': is_super_group,
                                'participants_count': conversation.entity.participants_count,
                                'deep_crwal': False
                            }
                        )
                    else:
                        TelegramGroup.objects.update_or_create(
                            id=conversation.id,
                            defaults={
                                'title': conversation.title,
                                'is_super_group': False,
                                'participants_count': conversation.entity.participants_count
                            }
                        )
                    telegram_account.groups.add(conversation.id)
                elif isinstance(conversation.entity, User):
                    if conversation.entity.bot == True:
                        continue
                    TelegramUser.objects.update_or_create(
                        id=conversation.entity.id,
                        defaults={
                            'username': conversation.entity.username,
                            'first_name': conversation.entity.first_name,
                            'last_name': conversation.entity.last_name,
                            'phone_number': conversation.entity.phone
                        }
                    )
                bar()
            except Exception as e:
                print(e)

def clean_db():
    TelegramGroup.objects.filter(participants_count=0).delete()
    TelegramUser.objects.filter(username=None,first_name=None,last_name=None,phone_number=None).delete()

def clean_channel(client: TelegramClient):
    conversations = client.iter_dialogs()
    for conversation in conversations:
        if hasattr(conversation.entity, 'broadcast'):
            if conversation.entity.broadcast == True:
                try:
                    TelegramGroup.objects.get(id=conversation.id).delete()
                except:
                    continue


def get_users_in_group(client: TelegramClient):
    groups = TelegramGroup.objects.all()
    for group in groups:
        users = client.get_participants(group.id)
        with alive_bar(len(users), title=group.title) as bar:
            for user in users:
                try:
                    if user.bot != True:
                        TelegramUser.objects.update_or_create(
                            id=user.id,
                            defaults={
                                'username': user.username,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'phone_number': user.phone
                            }
                        )
                        group.members.add(user.id)
                    bar()
                except Exception as e:
                    print(e)

def check_group_deep_crawl(client: TelegramClient):
    groups = TelegramGroup.objects.filter(is_super_group=True, deep_crwal=False)
    with alive_bar(len(groups)) as bar:
        for group in groups:
            if group.is_super_group == True:
                participants_count = len(client.get_participants(group.id))
                if participants_count < group.participants_count:
                    group.deep_crwal = True
                    group.save()
            bar()

def get_users_in_group_with_message(client: TelegramClient):
    groups = TelegramGroup.objects.filter(is_super_group=True, deep_crwal=True)
    for group in groups:
        messages = client.iter_messages(group.id)
        with alive_bar(title=group.title) as bar:
            for message in messages:
                user = client.get_entity(message.sender_id)
                TelegramUser.objects.update_or_create(
                    id=user.id,
                    defaults={
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone_number': user.phone
                    }
                )
                group.members.add(user.id)
                time.sleep(0.5)
                bar()