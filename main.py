import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from langdetect import detect

from googletrans import Translator, constants
from pprint import pprint

logging.basicConfig(level=logging.INFO)
bot = Bot('6497650532:AAHdiZ81rvAWPrR4YKNNWCNvHVkT8tF9bww')
key = '4e6d61ae4db44512ac9184730232312'
dp = Dispatcher()
builder = InlineKeyboardBuilder()

translator = Translator()
language = 'uk'


def output_city(message, command):
    city = command.args
    translation = translator.translate(city, dest="en")
    url = f'https://api.weatherapi.com/v1/current.json?key=4e6d61ae4db44512ac9184730232312&q={translation.text.lower()}&aqi=no'
    weather_data = requests.get(url).json()
    checker = str(requests.get(url))
    if checker == '<Response [400]>':
        message.answer(
            "Такого міста немає, напишіть інше\n"
            "/weather <city>"
        )
    else:
        city = weather_data['location']['name']
        region = weather_data['location']['region']
        country = weather_data['location']['country']
        builder.add(InlineKeyboardButton(
            text="Детальніше",
            url=f"https://www.timeanddate.com/weather/{country.lower()}/{city.lower()}")
        )
        trans_city = translator.translate(city, dest=language)
        trans_region = translator.translate(region, dest=language)
        trans_country = translator.translate(country, dest=language)
        time = weather_data['location']['localtime']
        temperature = round(weather_data['current']['temp_c'])
        feels_like = round(weather_data['current']['feelslike_c'])
        last_update_time = weather_data['current']['last_updated']

        message.answer(
            f"<b>Місцезнаходження:</b>\n"
            f"<b>Місто:</b> {trans_city.text}\n"
            f"<b>Регіон:</b> {trans_region.text}\n"
            f"<b>Країна:</b> {trans_country.text}\n"
            f"<b>Час зараз:</b> {time}\n"
            f"<b>Погода:</b>\n"
            f"<b>Температура:</b> {temperature} °C\n"
            f"<b>Відчувається як:</b> {feels_like} °C\n"
            f"<b>Оновлено:</b> {last_update_time}\n",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.HTML
        )


@dp.message(Command("start"))
async def cmd_weather(
        message: Message
):
    await message.answer(
        f"Вітаю {message.chat.first_name}!\n"
        f"Цей бот дає інформацію про погоду в усіх містах СВІТУ\n"
        f"Для цього потрібно написати команду /weather МІСТО\n"
    )


@dp.message(Command("help"))
async def cmd_help(
        message: Message
):
    await message.answer(
        "Усі команди:\n"
        "/start\n"
        "/weather МІСТО\n"
        "/lang\n"
    )


@dp.message(Command("lang"))
async def cmd_lang(
        message: Message
):
    await message.answer(
        "Pinus"
    )


@dp.message(Command("weather"))
async def cmd_weather(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            "Введіть назву міста!"

        )
    else:
        output_city(message, command)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
