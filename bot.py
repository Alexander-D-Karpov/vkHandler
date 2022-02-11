import os
import typing

import django
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

os.environ['DJANGO_SETTINGS_MODULE'] = 'vkHandler.settings'
django.setup()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData

from tg_bot.models import UserTag
from tg_bot.models import User
from callback.models import Tag

API_TOKEN = '5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

tag_cb = CallbackData('tag', 'tg')


@database_sync_to_async
def _get_tags():
    return Tag.objects.values('tags')


@database_sync_to_async
def _get_inline_tags() -> types.InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup()
    text_and_data = ([(x.name, x.name) for x in Tag.objects.all()])
    for i in range(0, len(text_and_data), 3):
        dat = (types.InlineKeyboardButton(text, callback_data=tag_cb.new(tg=data)) for text, data in text_and_data[i:i+3])
        keyboard_markup.row(*dat)
    return keyboard_markup


def _get_user(uuid: int) -> User:
    return User.objects.get(uuid=uuid)


@dp.message_handler(commands=['start'])
async def init(message: types.Message):
    user = await sync_to_async(User.objects.get_or_create, thread_sensitive=True) \
        (uuid=message.chat.id, username=message.chat.username)
    await message.reply(f"Hi, @{message.chat.username}")


@dp.message_handler(commands=['tags'])
async def init(message: types.Message):
    await message.reply("kjlkjl", reply_markup=await _get_inline_tags())


@dp.callback_query_handler(tag_cb.filter(tg=await _get_tags()))
async def callback_tag_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    await query.answer()
    tag = callback_data['tg']
    print(tag)


@dp.errors_handler(exception=MessageNotModified)  # handle the cases when this exception raises
async def message_not_modified_handler(update, error):
    return True


if __name__ == '__main__':
    executor.start_polling(dp)
