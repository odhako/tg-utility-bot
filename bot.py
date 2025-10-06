import logging
# logging - DEBUG, INFO, WARNING
logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)

from dotenv import load_dotenv
import os
from telethon import TelegramClient, events, Button
from telethon.tl.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

import db_functions
import pickle

# log in
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
api_id = int(os.environ.get('api_id'))
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')
bot = TelegramClient('bot', api_id, api_hash)


keyboard_inline = [
    Button.inline('hello', b'hello'),
    Button.inline('start', b'start'),
    Button.inline('stop', b'stop'),
]


public_from = 'oddevtst'
public_to = 'odddevtst2'
# scheduled_posts = []
schedule_active = False


@bot.on(events.NewMessage(pattern='/start', chats='odhako'))
async def start_handler(event):
    sender = await event.get_sender()
    all_posts = db_functions.get_all_posts_from_db()
    hello_message = f'Hello! There is {len(all_posts)} posts in schedule. Waiting for start...'
    await bot.send_message(sender, hello_message, buttons=keyboard_inline)


@bot.on(events.CallbackQuery(data=b'hello'))
async def button_handler(event):
    await event.answer('nice try')
    await event.edit('edited????', buttons=keyboard_inline)


@bot.on(events.CallbackQuery(data=b'start'))
async def button_handler(event):
    global schedule_active
    await event.answer('schedule ACTIVATED')
    schedule_active = True


@bot.on(events.CallbackQuery(data=b'stop'))
async def button_handler(event):
    global schedule_active
    await event.answer('schedule deactivated')
    schedule_active = False


@bot.on(events.NewMessage(incoming=True, chats='odhako'))
async def forward_handler(event):
    if not event.grouped_id:
        print('message!')
    else:
        print('from album')


@bot.on(events.Album(chats='odhako'))
async def album_handler(event):
    if not event.grouped_id:
        print('something wrong')
    else:
        print('album!')


@bot.on(events.NewMessage(incoming=True, chats=public_from))
async def schedule_handler(event):
    print('event.message = ', event.message)
    message_blob = pickle.dumps(event.message)
    print(message_blob)
    # db_functions.add_post_to_db(event.message)
    # logging.info('Post added to database')


# async def cron():
#     global schedule_active
#     if schedule_active:
#         logging.debug('Schedule is active - attempting to grab a post...')
#         grabbed_post = db_functions.pop_post_from_db()
#         await bot.send_message(entity=public_to, message=grabbed_post)
#     else:
#         logging.debug("Schedule isn't active - waiting for activation...")


async def main():
    await bot.start(bot_token=bot_token)
    scheduler.start()
    print("Scheduler started...\n(Press Ctrl+C to stop this)")
    await bot.run_until_disconnected()


scheduler = AsyncIOScheduler()
# scheduler.add_job(cron, 'interval', seconds=10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
