from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.types import Chat, User, Channel
from scraper.models import TelegramGroup, TelegramAccount, TelegramUser
from marketing.models import MarketingPlan
from alive_progress import alive_bar
import time
import asyncio

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

def get_users_in_group_with_message(client: TelegramClient):
    groups = TelegramGroup.objects.filter(is_super_group=True, deep_crwal=True)
    for group in groups:
        messages = client.iter_messages(group.id)
        with alive_bar(title=group.title) as bar:
            for message in messages:
                try:
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
                except Exception as e:
                    print(e)
                    time.sleep(150)
                    print("start again")
                bar()

def invite_users_to_channel(client: TelegramClient, marketing_plan: MarketingPlan):
    channel = client.get_entity(marketing_plan.target_group.username)
    for group in marketing_plan.selected_group.all():
        users = TelegramUser.objects.filter(groups__id=group.id, can_join_groups=True).order_by('id')
        for user in users:
            time.sleep(2)
            try:
                if user.username == None:
                    user_entity = client.get_entity(user.id)
                    client(InviteToChannelRequest(channel, [user_entity]))
                else:
                    client(InviteToChannelRequest(channel, [user.username]))
                print("Adding {} to {}".format(user.username, marketing_plan.target_group.title))
            except Exception as e:
                print('Failed to add {} to {}'.format(user.username, marketing_plan.target_group.title))
                if 'privacy' in str(e):
                    print("user privacy banned from adding to group")
                    user.can_join_groups = False
                    user.save()
                    continue
                elif 'Bots' in str(e):
                    print("user is bot")
                    user.can_join_groups = False
                    user.is_bot = True
                    user.save()
                    continue
                elif 'too many channels/supergroups' in str(e):
                    print("user is spam")
                    user.is_spam = True
                    user.save()
                    continue
                elif 'A wait of' in str(e) or 'Too many requests' in str(e):
                    print(e)
                    print("too many request 30 min")
                    time.sleep(1800)
                    continue
                else:
                    print(e)
                    print("another error")
                    continue

def invite_user_to_group(client: TelegramClient, selected_group):
    pass

def send_message_to_user(client: TelegramClient, marketing_plan: MarketingPlan):
    for group in marketing_plan.selected_group.all():
        users = TelegramUser.objects.filter(groups__id=group.id, can_join_groups=True).order_by('id')
        for user in users:
            time.sleep(2)
            try:
                if user.username == None:
                    user_entity = client.get_entity(user.id)
                    client.send_message(entity=user_entity,message=marketing_plan.message)
                else:
                    user_entity = client.get_entity(user.id)
                    client.send_message(entity=user_entity,message=marketing_plan.message)
                print("Sending message to {}".format(user.username))
            except Exception as e:
                print('Failed to send message to {}'.format(user.username))
                if 'privacy' in str(e):
                    print("user privacy banned from adding to group")
                    user.can_join_groups = False
                    user.save()
                    continue
                elif 'Bots' in str(e):
                    print("user is bot")
                    user.can_join_groups = False
                    user.is_bot = True
                    user.save()
                    continue
                elif 'too many channels/supergroups' in str(e):
                    print("user is spam")
                    user.is_spam = True
                    user.save()
                    continue
                elif 'A wait of' in str(e) or 'Too many requests' in str(e):
                    print(e)
                    print("too many request 30 min")
                    time.sleep(1800)
                    continue
                else:
                    print(e)
                    print("another error")
                    continue
