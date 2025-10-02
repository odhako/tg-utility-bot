import asyncio
import logging
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


# loading from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# logging
logging.basicConfig(level=logging.INFO)

# bot object
TOKEN = os.environ.get('TOKEN')
bot = Bot(TOKEN)

# dispatcher
dp = Dispatcher()


# handlers
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello, world!')


# polling
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
