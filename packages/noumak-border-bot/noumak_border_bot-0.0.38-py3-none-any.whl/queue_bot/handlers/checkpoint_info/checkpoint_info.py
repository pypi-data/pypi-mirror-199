from aiogram import types
from queue_bot.base.parser import Parser
from queue_bot.bot import dp
from queue_bot import keyboard
from queue_bot.utils.anti_flod import flood_commands
from queue_bot.middleware import _


@dp.message_handler(commands=["beniakoni_info"])
@dp.throttled(flood_commands, rate=2)
async def beniakoni_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Гродненская область, Вороновский район, деревня Бенякони</i>\n"
            "<b>Телефон: </b><i>+375 (33) 654-22-04, +375 (15) 944-60-30 </i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["berestovitsa_info"])
@dp.throttled(flood_commands, rate=2)
async def berestovitsa_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Гродненская обл., Берестовицкий р-н, ГП Пограничный (ПП Берестов. — Бобровники)</i>\n"
            "<b>Телефон: </b><i>+375 (33) 654-22-88,+375 (33) 654-22-15</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["brest_info"])
@dp.throttled(flood_commands, rate=2)
async def brest_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Брест, Варшавское шоссе, 1</i>\n"
            "<b>Телефон: </b><i>+375(29) 155-56-44, +375(33) 686-06-86</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["grigorovshcina_info"])
@dp.throttled(flood_commands, rate=2)
async def grigorovshcina_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Витебская область, Верхнедвинский район,Бигосовский сельсовет, деревня Григоровщина</i>\n"
            "<b>Телефон: </b><i>+375(29) 200-97-71</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["kamenny_log_info"])
@dp.throttled(flood_commands, rate=2)
async def kamenny_log_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Гродненская обл., Ошмянский район, М7, 147км, 4</i>\n"
            "<b>Телефон: </b><i>+375 (1593) 49-920, +375 33 370-4265</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["kotlovka_info"])
@dp.throttled(flood_commands, rate=2)
async def kotlovka_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Гродненская область, Островецкий район, Ворнянский сельсовет, деревня Котловка</i>\n"
            "<b>Телефон: </b><i>+375(15) 917-59-01</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )


@dp.message_handler(commands=["urbany_info"])
@dp.throttled(flood_commands, rate=2)
async def urbany_info(message: types.Message):
    await message.answer(
        text=_(
            "<b>Адрес: </b><i>Витебская область, Браславский район, Межанский сельсовет, деревня Урбаны</i>\n"
            "<b>Телефон: </b><i>+375(215) 36-70-27</i>"
        ),
        parse_mode="html",
        reply_markup=keyboard.ikb_menu(),
    )
