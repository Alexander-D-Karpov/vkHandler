import os
import sqlite3
import django
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import datetime

os.environ["DJANGO_SETTINGS_MODULE"] = "vkHandler.settings"
django.setup()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from tg_bot.models import UserTag, UserAttend
from tg_bot.models import User
from callback.models import Tag, Post

API_TOKEN = "5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

tag_cb = CallbackData("tag", "tg")


def _get_tags():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    re = []
    for row in cur.execute("SELECT name FROM callback_tag"):
        re.append(row[0])
    return re


@database_sync_to_async
def _get_upcoming_posts():
    return [x for x in Post.objects.all() if x.date and (datetime.tim(x.date.strftime('%Y-%m-%d')) >= datetime.date(datetime.date.today()))]


@database_sync_to_async
def _get_inline_tags(uuid: int) -> types.InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup()
    text_and_data = []
    for tag in Tag.objects.all():
        if UserTag.objects.filter(user__uuid=uuid, tag=tag).exists():
            text_and_data.append(("✅ " + tag.name, tag.name))
        else:
            text_and_data.append((tag.name, tag.name))

    for i in range(0, len(text_and_data), 3):
        dat = []
        for text, data in text_and_data[i: i + 3]:
            call = tag_cb.new(tg=data)
            dat.append(types.InlineKeyboardButton(text, callback_data=call))
        keyboard_markup.row(*dat)
    return keyboard_markup


@database_sync_to_async
def _get_user(uuid: int) -> User:
    return User.objects.get(uuid=uuid)


@database_sync_to_async
def _get_post(post_id: int) -> Post:
    return Post.objects.get(id=post_id)


@database_sync_to_async
def _create_or_delete_user_tag(uuid: int, tag: str) -> None:
    user = User.objects.get(uuid=uuid)
    tag = Tag.objects.get(name=tag)
    try:
        UserTag.objects.get(user=user, tag=tag).delete()
    except UserTag.DoesNotExist:
        UserTag.objects.create(user=user, tag=tag)


@database_sync_to_async
def _prepare_user_attend(post_id: int, user_id: int):
    keyboard_markup = types.InlineKeyboardMarkup()
    if UserAttend.objects.filter(user__uuid=user_id, post_id=post_id).exists():
        UserAttend.objects.get(post_id=post_id, user_id=user_id).delete()
        keyboard_markup.add(
            types.InlineKeyboardButton("Записаться", callback_data=f"post:{post_id}")
        )
    else:
        UserAttend.objects.create(post_id=post_id, user_id=user_id)
        keyboard_markup.add(
            types.InlineKeyboardButton("Отписаться", callback_data=f"post:{post_id}")
        )
    return keyboard_markup


button1 = KeyboardButton('Тэги')
button2 = KeyboardButton('Предстоящие мероприятия')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2)


@dp.message_handler(commands=["start"])
async def init(message: types.Message):
    await sync_to_async(User.objects.get_or_create, thread_sensitive=True)(
        uuid=message.chat.id, username=message.chat.username
    )
    await message.reply(f"Hi, @{message.chat.username}", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Тэги")
async def init(message: types.Message):
    await message.reply(
        "Подписаться на тэги", reply_markup=await _get_inline_tags(uuid=message.chat.id)
    )


#   @dp.message_handler(lambda message: message.text == "Предстоящие мероприятия")
#async def init(message: types.Message):
    #await message.reply(
    #    await _get_upcoming_posts()
    #)


@dp.callback_query_handler(lambda call: True)
async def callback_action(query: types.CallbackQuery):
    await query.answer()
    data = query.data.split(":")
    if data[0] == "tag":
        tag = data[1]

        await _create_or_delete_user_tag(query.from_user.id, tag)

        await bot.edit_message_text(
            "Подписаться на тэги",
            query.from_user.id,
            query.message.message_id,
            reply_markup=await _get_inline_tags(uuid=query.message.chat.id),
        )
    elif data[0] == "post":
        markup = await _prepare_user_attend(int(data[1]), query.from_user.id)

        await bot.edit_message_text(
            query.message.text,
            query.from_user.id,
            query.message.message_id,
            reply_markup=markup,
        )


@dp.errors_handler(
    exception=MessageNotModified
)  # handle the cases when this exception raises
async def message_not_modified_handler(update, error):
    return True


if __name__ == "__main__":
    executor.start_polling(dp)
