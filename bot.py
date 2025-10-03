import logging
# logging - DEBUG, INFO, WARNING
logging.basicConfig(format='[%(levelname)s %(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)

from dotenv import load_dotenv
import os
import ssl
from telethon import TelegramClient, events, Button


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


keyboard_text = [
    Button.text('hello', resize=True),
    Button.text('button'),
    Button.text('cool'),
]

keyboard_inline = [
    Button.inline('hello', b'hello'),
    Button.inline('button', b'button'),
    Button.inline('cool', b'cool'),
]


@bot.on(events.NewMessage)
async def message_handler(event):
    sender = await event.get_sender()
    if 'hello' in event.raw_text:
        await bot.send_message(sender, 'hi', buttons=keyboard_inline)


@bot.on(events.CallbackQuery(data=b'hello'))
async def button_handler(event):
    print('hello')
    await event.answer('nice try')
    await event.edit('edited????', buttons=keyboard_inline)

    # if event.data == 'button':
    #     print('button')
    #     await bot.edit_message(sender, 'the button was pressed', buttons=keyboard_inline)
    # if event.data == 'cool':
    #     print('cool')
    #     await bot.edit_message(sender, 'so you are!', buttons=keyboard_inline)


bot.start()
bot.run_until_disconnected()
