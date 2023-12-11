from scraper.src import crawl

COMMON_JOB = {
    'sc': crawl.get_conversations,
    'sug': crawl.get_users_in_group,
    'sugm': crawl.get_users_in_group_with_message,
    'iuc': crawl.invite_users_to_channel,
    'iug': crawl.invite_user_to_group,
    'smu': crawl.send_message_to_user,
}