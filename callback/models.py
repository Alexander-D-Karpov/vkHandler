from django.db import models
from tg_bot.models import User, UserTag
import telebot

# Create your models here.

token = '5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA'


def send_at_all(msg, tags):
    bot = telebot.TeleBot(token)
    users = []
    for tag in tags:
        for user in UserTag.objects.filter(name=tag):
            if not user.user in users:
                users.append(user.user)
    for user in users:
        bot.send_message(user.uuid, msg)


class Post(models.Model):
    object = models.JSONField()
    event_id = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        tags = []
        text = []
        check_tags = []

        for tag in Tag.objects.all():
            for xtag in tag.tags.split(" "):
                check_tags.append(xtag)

        for line in self.object['text'].split("\n"):
            for tag in check_tags:
                if tag in line and not tag in tags:
                    tags.append(tag)
            l = " ".join(filter(lambda x: x[0] != '#', line.split()))
            if l != "":
                text.append(l)

        text = "\n".join(text)
        send_at_all(text, tags)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.object['text']


class Tag(models.Model):
    name = models.CharField(max_length=50)
    tags = models.TextField(blank=False)

    def __str__(self):
        return self.name
