import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

from googletrans import Translator

logging.basicConfig(level=logging.INFO)
bot = Bot('6497650532:AAHdiZ81rvAWPrR4YKNNWCNvHVkT8tF9bww')
key = '4e6d61ae4db44512ac9184730232312'
dp = Dispatcher()

translator = Translator()
language = 'uk'


@dp.message(Command("lang"))
async def cmd_lang(
        lang_message: Message
):
    trans_choice_lang = translator.translate("Виберіть мову", dest=language)
    trans_ukr = translator.translate("🇺🇦Українська мова", dest=language)
    trans_eng = translator.translate("🇺🇸Англійська мова", dest=language)
    trans_rus = translator.translate("🇷🇺Російська мова", dest=language)
    trans_pol = translator.translate("🇵🇱Польска мова", dest=language)

    kb = [
        [
            KeyboardButton(text=f"{trans_ukr.text}"),
            KeyboardButton(text=f"{trans_eng.text}"),
        ],
        [
            KeyboardButton(text=f"{trans_rus.text}"),
            KeyboardButton(text=f"{trans_pol.text}")
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=trans_choice_lang.text
    )
    await lang_message.answer(
        f"{trans_choice_lang.text}:",
        reply_markup=keyboard,
    )

    @dp.message(F.text.lower() == f"{trans_ukr.text.lower()}")
    async def ukr(lang_message: Message):
        global language
        language = 'uk'
        await lang_message.reply("Вибрано українську мову", reply_markup=ReplyKeyboardRemove())
        return language

    @dp.message(F.text.lower() == f"{trans_eng.text.lower()}")
    async def eng(lang_message: Message):
        global language
        language = 'en'
        await lang_message.reply("English is selected", reply_markup=ReplyKeyboardRemove())
        return language

    @dp.message(F.text.lower() == f"{trans_rus.text.lower()}")
    async def rus(lang_message: Message):
        global language
        language = 'ru'
        await lang_message.reply("Выбран русский язык", reply_markup=ReplyKeyboardRemove())
        return language

    @dp.message(F.text.lower() == f"{trans_pol.text.lower()}")
    async def pol(lang_message: Message):
        global language
        language = 'pl'
        await lang_message.reply("Wybrano język polski", reply_markup=ReplyKeyboardRemove())
        return language

    return


async def output_city(message, command):
    print(language)
    city = command.args
    translation = translator.translate(city, dest="en")
    url = f'https://api.weatherapi.com/v1/current.json?key=4e6d61ae4db44512ac9184730232312&q={translation.text.lower()}&aqi=no'
    weather_data = requests.get(url).json()
    checker = str(requests.get(url))
    if checker == '<Response [400]>':
        trans_error = translator.translate("Такого міста немає, напишіть інше", dest=language)
        await message.answer(
            f"{trans_error.text}\n"
            "/weather <city>"
        )
    else:
        city = weather_data['location']['name']
        region = weather_data['location']['region']
        country = weather_data['location']['country']
        builder = InlineKeyboardBuilder()
        trans_detail = translator.translate("Детальніше", dest=language)
        builder.row(InlineKeyboardButton(
            text=f"{trans_detail.text}",
            url=f"https://www.timeanddate.com/weather/{country.lower()}/{city.lower()}")
        )
        trans_city = translator.translate(city, dest=language)
        trans_region = translator.translate(region, dest=language)
        trans_country = translator.translate(country, dest=language)
        time = weather_data['location']['localtime']
        temperature = round(weather_data['current']['temp_c'])
        feels_like = round(weather_data['current']['feelslike_c'])
        last_update_time = weather_data['current']['last_updated']

        trans_contain_location = translator.translate("Місцезнаходження", dest=language)
        trans_contain_city = translator.translate("Місто", dest=language)
        trans_contain_region = translator.translate("Регіон", dest=language)
        trans_contain_country = translator.translate("Країна", dest=language)
        trans_contain_time = translator.translate("Час зараз", dest=language)
        trans_contain_weather = translator.translate("Погода", dest=language)
        trans_contain_temperature = translator.translate("Температура", dest=language)
        trans_contain_feels_like = translator.translate("Відчувається як", dest=language)
        trans_contain_last_update_time = translator.translate("Оновлено", dest=language)

        await message.answer(
            f"<b>{trans_contain_location.text}:</b>\n"
            f"<b>{trans_contain_city.text}:</b> {trans_city.text}\n"
            f"<b>{trans_contain_region.text}:</b> {trans_region.text}\n"
            f"<b>{trans_contain_country.text}:</b> {trans_country.text}\n"
            f"<b>{trans_contain_time.text}:</b> {time}\n"
            f"<b>{trans_contain_weather.text}:</b>\n"
            f"<b>{trans_contain_temperature.text}:</b> {temperature} °C\n"
            f"<b>{trans_contain_feels_like.text}:</b> {feels_like} °C\n"
            f"<b>{trans_contain_last_update_time.text}:</b> {last_update_time}\n",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.HTML
        )


@dp.message(Command("start"))
async def cmd_weather(
        message: Message
):
    trans_hello = translator.translate("Привіт", dest=language)
    trans_message_first = translator.translate("Цей бот дає інформацію про погоду в усіх містах СВІТУ", dest=language)
    trans_message_second = translator.translate("Для цього потрібно написати команду", dest=language)
    trans_city = translator.translate("<Місто>", dest=language)
    await message.answer(
        f"{trans_hello.text} {message.chat.first_name}!\n"
        f"{trans_message_first.text}\n"
        f"{trans_message_second.text} /weather {trans_city.text}\n",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command("help"))
async def cmd_help(
        message: Message
):
    trans_commands = translator.translate("Усі команди", dest=language)
    trans_city = translator.translate("<Місто>", dest=language)
    await message.answer(
        f"{trans_commands.text}:\n"
        "/start\n"
        f"/weather {trans_city.text}\n"
        "/lang\n",
        reply_markup=ReplyKeyboardRemove()
    )


async def main():
    await dp.start_polling(bot)


@dp.message(Command("weather"))
async def cmd_weather(
        message: Message,
        command: CommandObject,
):
    trans_choice = translator.translate("Введіть", dest=language)
    trans_city = translator.translate("<Місто>!", dest=language)
    if command.args is None:
        await message.reply(
            f"{trans_choice.text} /weather {trans_city.text}\n",
            reply_markup=ReplyKeyboardRemove()
        )
        # @dp.message(F.text)
        # async def get_city(
        #         city: Message):
        #     city_command = CommandObject(prefix='/', command='weather', mention=None, args=city.text)
        #
        #     await output_city(city, city_command)
        #     return
    else:
        trans_search = translator.translate("Пошук", dest=language)
        await message.answer(f"{trans_search.text}...", reply_markup=ReplyKeyboardRemove())
        await output_city(message, command)
    return


if __name__ == "__main__":
    asyncio.run(main())
