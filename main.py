import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from datetime import datetime

from googletrans import Translator

logging.basicConfig(level=logging.INFO)
bot = Bot('6497650532:AAHdiZ81rvAWPrR4YKNNWCNvHVkT8tF9bww')
key = '4e6d61ae4db44512ac9184730232312'
dp = Dispatcher()

translator = Translator()
language = 'ru'


@dp.message(Command("start"))
async def cmd_weather(
        message: Message
):
    trans_hello = translator.translate("Привет", dest=language)
    trans_message_first = translator.translate("Этот бот дает информацию о погоде во всем МИРЕ.", dest=language)
    trans_message_second = translator.translate("Для этого нужно написать команду", dest=language)
    trans_city = translator.translate("<Город>", dest=language)
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
    trans_commands = translator.translate("Все команды", dest=language)
    trans_city = translator.translate("<Город>", dest=language)
    await message.answer(
        f"{trans_commands.text}:\n"
        "/start\n"
        f"/weather {trans_city.text}\n"
        "/lang\n",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command("lang"))
async def cmd_lang(
        lang_message: Message
):
    trans_choice_lang = translator.translate("Выберите язык", dest=language)
    trans_rus = translator.translate("🇷🇺Русский язык", dest=language)
    trans_eng = translator.translate("🇺🇸Английский язык", dest=language)
    trans_ukr = translator.translate("🇺🇦Украинский язык", dest=language)
    trans_pol = translator.translate("🇵🇱Польский язык", dest=language)
    trans_chi = translator.translate("🇨🇳Китайский язык", dest=language)
    trans_kaz = translator.translate("🇰🇿Казахский язык", dest=language)

    kb = [
        [
            KeyboardButton(text=f"{trans_rus.text}"),
            KeyboardButton(text=f"{trans_eng.text}"),
            KeyboardButton(text=f"{trans_chi.text}"),
        ],
        [
            KeyboardButton(text=f"{trans_kaz.text}"),
            KeyboardButton(text=f"{trans_ukr.text}"),
            KeyboardButton(text=f"{trans_pol.text}")
        ],
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

    @dp.message(F.text.lower() == f"{trans_kaz.text.lower()}")
    async def ukr(lang_message: Message):
        global language
        language = 'kk'
        await lang_message.reply("Орыс тілі таңдалды", reply_markup=ReplyKeyboardRemove())
        return language

    @dp.message(F.text.lower() == f"{trans_chi.text.lower()}")
    async def ukr(lang_message: Message):
        global language
        language = 'zh-cn'
        await lang_message.reply("选择俄语", reply_markup=ReplyKeyboardRemove())
        return language

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


@dp.message(Command("weather"))
async def cmd_weather(
        message: Message,
        command: CommandObject,
):
    trans_choice = translator.translate("Введите", dest=language)
    trans_city = translator.translate("<Город>!", dest=language)
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
        trans_search = translator.translate("Поиск", dest=language)
        await message.answer(f"{trans_search.text}...", reply_markup=ReplyKeyboardRemove())
        await output_city(message, command)
    return


def format_time(input_time):
    dt = datetime.strptime(input_time, '%Y-%m-%d %H:%M')
    return dt.strftime('%d %B %Y %H:%M')


async def output_city(message, command):
    print(language)
    city = command.args
    translation = translator.translate(city, dest="en")
    url = f'https://api.weatherapi.com/v1/current.json?key=4e6d61ae4db44512ac9184730232312&q={translation.text.lower()}&aqi=no&lang={language}'
    print(url)
    weather_data = requests.get(url).json()
    checker = str(requests.get(url))
    if checker == '<Response [400]>':
        trans_error = translator.translate("Такого города нет, напишите другой", dest=language)
        await message.answer(
            f"{trans_error.text}\n"
            "/weather <city>"
        )
    else:
        city = weather_data['location']['name']
        region = weather_data['location']['region']
        country = weather_data['location']['country']
        weather = weather_data['current']['condition']['text']
        builder = InlineKeyboardBuilder()
        trans_detail = translator.translate("Подробнее", dest=language)
        builder.row(InlineKeyboardButton(
            text=f"{trans_detail.text}",
            url=f"https://www.timeanddate.com/weather/{country.lower()}/{city.lower()}")
        )
        trans_city = translator.translate(city, dest=language)
        trans_region = translator.translate(region, dest=language)
        trans_country = translator.translate(country, dest=language)
        trans_weather = translator.translate(weather, dest=language)
        time = weather_data['location']['localtime']
        temperature = round(weather_data['current']['temp_c'])
        feels_like = round(weather_data['current']['feelslike_c'])
        last_update_time = weather_data['current']['last_updated']

        trans_time = translator.translate(format_time(time), dest=language)
        trans_last_update_time = translator.translate(format_time(last_update_time), dest=language)

        trans_contain_location = translator.translate("Местонахождение", dest=language)
        trans_contain_city = translator.translate("Город", dest=language)
        trans_contain_region = translator.translate("Регион", dest=language)
        trans_contain_country = translator.translate("Страна", dest=language)
        trans_contain_time = translator.translate("Время сейчас", dest=language)
        trans_contain_weather = translator.translate("Погода", dest=language)
        trans_contain_temperature = translator.translate("Температура", dest=language)
        trans_contain_feels_like = translator.translate("Чувствуется как", dest=language)
        trans_contain_last_update_time = translator.translate("Обновлено", dest=language)

        if language != "ru":
            await message.answer(
                f"<b>{trans_contain_location.text}:</b>\n"
                f"<b>{trans_contain_city.text}:</b> {trans_city.text}\n"
                f"<b>{trans_contain_region.text}:</b> {trans_region.text}\n"
                f"<b>{trans_contain_country.text}:</b> {trans_country.text}\n"
                f"<b>{trans_contain_time.text}:</b> {trans_time.text}\n"
                f"<b>{trans_contain_weather.text}: {trans_weather.text}</b>\n"
                f"<b>{trans_contain_temperature.text}:</b> {temperature} °C\n"
                f"<b>{trans_contain_feels_like.text}:</b> {feels_like} °C\n"
                f"<b>{trans_contain_last_update_time.text}:</b> {trans_last_update_time.text}\n",
                reply_markup=builder.as_markup(),
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                f"<b>Местонахождение:</b>\n"
                f"<b>Город:</b> {trans_city.text}\n"
                f"<b>Регион:</b> {trans_region.text}\n"
                f"<b>Страна:</b> {trans_country.text}\n"
                f"<b>Время сейчас:</b> {trans_time.text}\n"
                f"<b>Погода: {trans_weather.text}</b>\n"
                f"<b>Температура:</b> {temperature} °C\n"
                f"<b>Чувствуется как:</b> {feels_like} °C\n"
                f"<b>Обновлено:</b> {trans_last_update_time.text}\n",
                reply_markup=builder.as_markup(),
                parse_mode=ParseMode.HTML
            )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
