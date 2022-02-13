import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback.models import Post, PostTag
from tg_bot.models import UserTag

API_TOKEN = "5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA"
bot = telebot.TeleBot(API_TOKEN)


def _gen_markup(data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Записаться", callback_data=f"post:{data}"))
    return markup


def send_at_all(post: Post):
    markup = _gen_markup(post.id)
    users = []
    for user in UserTag.objects.filter(
        tag__in=[x.tag for x in PostTag.objects.filter(post=post)]
    ):
        u = user.user.uuid
        if u not in users:
            users.append(u)

    for user in users:
        bot.send_message(user, post.text, reply_markup=markup)
