import telebot
import kronos
import datetime

from tg_bot.models import UserAttend

API_TOKEN = "5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA"
bot = telebot.TeleBot(API_TOKEN)


@kronos.register('30 8 * * *')
def send_post_cron():
    users = {}
    for attend in UserAttend.objects.all():
        if attend.post.date and attend.post.date.strftime('%Y-%m-%d') == datetime.date.today().strftime('%Y-%m-%d'):
            if attend.user.uuid not in users:
                users[attend.user.uuid] = "Доброе утро!\nНапоминаем что сегодня пройдет:\n"
            users[attend.user.uuid] += attend.post.text[:50] + ("... " if len(attend.post.text) > 50 else " ")\
                                       + attend.post.link + "\n\n"

    for user in users:
        bot.send_message(user, users[user])
