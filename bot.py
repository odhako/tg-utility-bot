from dotenv import load_dotenv
import os
from telethon import TelegramClient, events
import logging


# logging - set INFO of WARNING
logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)


# log in
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
api_id = int(os.environ.get('api_id'))
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


# single message
# with bot:
#     bot.loop.run_until_complete(bot.send_message('@odhako', 'Hello, myself!'))
#     bot.loop.run_until_complete(bot.send_file('@odhako', 'test_files/001.jpg'))

# many messages
# async def main():
#     await bot.send_message('odhako', 'many test1')
#     await bot.send_message('odhako', 'many test2')
#     await bot.send_message('odhako', 'many test3')
# with bot:
#     bot.loop.run_until_complete(main())

@bot.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

bot.start()
bot.run_until_disconnected()
