import logging

import redis
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


class KVStorage:
    def __init__(self):
        self.r = redis.Redis(host='db', port=6969, db=0, password='underwaterlove')

    async def store(self, key: str, value: str):
        self.r.set(key, value)

    async def load(self, key: str):
        return self.r.get(key)


API_TOKEN = open('tg_token').read().strip()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
storage = KVStorage()

HELP_MESSAGE = """Usage:
!set key value
!get key
"""


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(HELP_MESSAGE)


@dp.message_handler()
async def echo(message: types.Message):
    command = message.text.split()
    if len(command) == 1:
        await message.reply(HELP_MESSAGE)
        return
    if command[0] == '!set':
        if len(command) != 3:
            await message.reply(HELP_MESSAGE)
            return
        k, v = command[1], command[2]
        await storage.store(k, v)
        await message.reply("Successfully stored!")
    elif command[0] == '!get':
        if len(command) != 2:
            await message.reply(HELP_MESSAGE)
            return
        k = command[1]
        v = await storage.load(k)
        if v is None:
            await message.reply("Not found!")
        else:
            await message.reply(v)
    else:
        await message.reply(HELP_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
