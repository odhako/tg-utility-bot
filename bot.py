from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from telethon import TelegramClient, events, Button

from settings import settings
import db_functions

import logging
# logging - DEBUG, INFO, WARNING
logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)


# log in
bot = TelegramClient('bot', settings.api_id, settings.api_hash, catch_up=True)


# variables
admin = settings.admin
public_from = settings.public_from
public_to = settings.public_to


# creating db - if not exists
DB = settings.database_file
db_functions.create_db(DB)

# main keyboard
keyboard_inline = [
    [
        Button.inline('hello', b'hello'),
        Button.inline('start', b'start'),
        Button.inline('stop', b'stop'),
    ],
    [
        Button.inline('pick and post now', b'pick_and_post_now'),
    ]
]


# handlers
@bot.on(events.NewMessage(pattern='/start', chats=admin))
async def start_handler(event):
    sender = await event.get_sender()
    all_posts = db_functions.get_all_posts_from_db(DB)
    hello_message = f'Hello! There is {len(all_posts)} posts in schedule. Waiting for start...'
    await bot.send_message(sender, hello_message, buttons=keyboard_inline)


@bot.on(events.CallbackQuery(data=b'hello', chats=admin))
async def hello_handler(event):
    await event.answer('hello and welcome!')


@bot.on(events.CallbackQuery(data=b'start', chats=admin))
async def start_handler(event):
    settings.start_schedule()
    await event.answer('schedule ACTIVATED')


@bot.on(events.CallbackQuery(data=b'stop', chats=admin))
async def stop_handler(event):
    settings.stop_schedule()
    await event.answer('schedule deactivated')


@bot.on(events.CallbackQuery(data=b'pick_and_post_now', chats=admin))
async def post_message_handler(event):
    if db_functions.db_has_data(DB):
        post_id = db_functions.pop_post_from_db(DB)
        new_post = await bot.get_messages(public_from, ids=post_id)
        await bot.send_message(entity=public_to, message=new_post)
        await bot.delete_messages(entity=public_from, message_ids=post_id)
        await event.answer('posted!')
    else:
        await event.answer('error: db is empty')


@bot.on(events.NewMessage(incoming=True, chats=public_from))
async def schedule_handler(event):
    logging.info(f'New post to schedule: event.message.id = {event.message.id}')
    db_functions.add_post_to_db(DB, event.message.id)


# TODO: differ albums from single pictures
# @bot.on(events.NewMessage(incoming=True, chats=admin))
# async def forward_handler(event):
#     if not event.grouped_id:
#         print('message!')
#     else:
#         print('from album')
#
#
# @bot.on(events.Album(chats=admin))
# async def album_handler(event):
#     if not event.grouped_id:
#         print('something wrong')
#     else:
#         print('album!')


# job for APScheduler
async def auto_poster():
    if settings.schedule_active:
        logging.debug('Schedule is active - attempting to grab a post...')
        post_id_from_queue = db_functions.pop_post_from_db(DB)
        new_post = await bot.get_messages(public_from, ids=post_id_from_queue)
        await bot.send_message(entity=public_to, message=new_post)
        await bot.delete_messages(entity=public_from, message_ids=post_id_from_queue)
        logging.info('****** Auto poster: new post posted ******')
    else:
        logging.debug("Schedule isn't active - waiting for activation...")


# main loop
async def main():
    await bot.start(bot_token=settings.bot_token)
    scheduler.start()
    print("Scheduler started...\n(Press Ctrl+C to stop this)")
    await bot.run_until_disconnected()


# APScheduler initialization
scheduler = AsyncIOScheduler()
# scheduler.add_job(auto_poster, 'cron', hour='0,8,16', jitter=6000)
scheduler.add_job(auto_poster, 'interval', seconds='5')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
