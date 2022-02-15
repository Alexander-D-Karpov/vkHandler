import telebot

from callback.models import Post
from callback.services.send_at_all import send_at_all
import kronos
import datetime

from tg_bot.models import UserAttend

API_TOKEN = "5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA"
bot = telebot.TeleBot(API_TOKEN)


@kronos.register('30 8 * * *')
def send_post_cron():
    for attend in UserAttend.objects.all():
        print(attend.post.date.strftime('%Y-%m-%d'))
        print(datetime.date.today().strftime('%Y-%m-%d'))
        if attend.post.date.strftime('%Y-%m-%d') == datetime.date.today().strftime('%Y-%m-%d'):
            bot.send_message(attend.user.uuid, attend.post.text)
