from telethon.sync import TelegramClient
from telethon.functions import channels
from telethon.types import Chat, User
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
                if isinstance(conversation, Chat):
                    if hasattr(conversation.entity, 'megagroup'):
                        if conversation.entity.gigagroup == True:
                            continue
                        TelegramGroup.objects.update_or_create(
                            id=conversation.id,
                            defaults={
                                'title': conversation.title,
                                'is_super_group': True,
                                'participants_count': conversation.entity.participants_count
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
                elif isinstance(conversation, User):
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
                # time.sleep(0.5)
                bar()
            except Exception as e:
                print(e)


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
                        # time.sleep(0.3)
                    bar()
                except Exception as e:
                    print(e)


def get_users_in_group_with_message(client: TelegramClient):
    groups = TelegramGroup.objects.all()
    for group in groups:
        messages = client.get_messages(group.id)
        with alive_bar(len(messages), title=group.title) as bar:
            for message in messages:
                print(message)
                # TelegramUser.objects.update_or_create(
                #     id=user.id,
                #     defaults={
                #         'username': user.username,
                #         'first_name': user.first_name,
                #         'last_name': user.last_name,
                #         'phone_number': user.phone
                #     }
                # )
                # group.members.add(user.id)
                # time.sleep(0.5)
                # bar()