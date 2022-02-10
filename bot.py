import os
import django
from asgiref.sync import sync_to_async

os.environ['DJANGO_SETTINGS_MODULE'] = 'vkHandler.settings'
django.setup()

from aiogram import Bot, Dispatcher, executor, types
from tg_bot.models import UserTag
from tg_bot.models import User

API_TOKEN = '5048852247:AAE8g6zVHc229FBQ72zjM4baNJynOqullfA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def init(message: types.Message):
    user = await sync_to_async(User.objects.get_or_create, thread_sensitive=True) \
        (uuid=message.chat.id, username=message.chat.username)
    await message.reply(f"Hi, @{message.chat.username}")


if __name__ == '__main__':
    executor.start_polling(dp)
