import telebot

from callback.models import Post, PostTag
from tg_bot.models import UserTag

API_TOKEN = '5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA'
bot = telebot.TeleBot(API_TOKEN)


def send_at_all(post: Post):
    users = []
    for user in UserTag.objects.filter(tag__in=[x.tag for x in PostTag.objects.filter(post=post)]):
        u = user.user.uuid
        if u not in users:
            users.append(u)

    for user in users:
        bot.send_message(user, post.text)


