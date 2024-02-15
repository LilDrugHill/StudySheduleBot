import logging

import dotenv
import os
import aiogram
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

import Scripts.main
import Scripts.convertors

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher()

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Куда сейчас?")],
        [types.KeyboardButton(text="Расписание на сегодня/завтра")],
        [types.KeyboardButton(text="Расписание на неделю")],
        [types.KeyboardButton(text="Экзамены(надеюсь не зачеты)")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Слушаю...",
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=keyboard)


@dp.message(F.text.lower() == "расписание на неделю")
async def show_weekly(message: types.Message):
    await message.answer(
        Scripts.convertors.schedule_obj_2_str_week(Scripts.main.main()),
        parse_mode="html",
        reply_markup=keyboard,
    )


@dp.message(F.text.lower() == "расписание на сегодня/завтра")
async def show_daily(message: types.Message):
    await message.answer(
        Scripts.convertors.schedule_obj_2_str_day(Scripts.main.main()),
        parse_mode="html",
        reply_markup=keyboard,
    )


@dp.message(F.text.lower() == "куда сейчас?")
async def show_now(message: types.Message):
    await message.answer(
        Scripts.convertors.where_are_we_going_now(Scripts.main.main()),
        parse_mode="html",
        reply_markup=keyboard,
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
