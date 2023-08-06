from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from queue_bot.utils.anti_flod import flood_commands, flood_callback
from queue_bot import keyboard
from queue_bot.bot import dp, bot
from queue_bot.base.template import help_template, srart_template, tiket_template
from queue_bot.middleware import _


@dp.errors_handler(exception=MessageNotModified)
async def error(update: types.Update, exeptions: MessageNotModified):
    await bot.answer_callback_query(callback_query_id=update.callback_query.id)
    return True


@dp.message_handler(commands=["help"])
@dp.throttled(flood_commands, rate=2)
async def help_command(message: types.Message):
    await message.answer(
        text=help_template(), reply_markup=keyboard.ikb_tiket(), parse_mode="html"
    )


@dp.message_handler(commands=["start"])
@dp.throttled(flood_commands, rate=2)
async def start_command(message: types.Message):
    await message.answer(
        text=_("Выбери язык 👇"), reply_markup=keyboard.ikb_language(), parse_mode="html"
    )


@dp.message_handler(commands=["long"])
@dp.throttled(flood_commands, rate=2)
async def start_command(message: types.Message):
    await message.answer(
        text=_("Выбери язык 👇"), reply_markup=keyboard.ikb_language(), parse_mode="html"
    )


@dp.callback_query_handler(text=["ru", "en", "pl"])
@dp.throttled(flood_callback, rate=1)
async def ru(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=srart_template(), reply_markup=keyboard.ikb_menu()
    )


@dp.message_handler(commands=["tiket"])
@dp.throttled(flood_commands, rate=2)
async def start_command(message: types.Message):
    await message.answer(
        text=tiket_template(), reply_markup=keyboard.ikb_tiket(), parse_mode="html"
    )


@dp.callback_query_handler(text="checkpoint")
@dp.throttled(flood_callback, rate=1)
async def checkpoint(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Выберите нужную границу"), reply_markup=keyboard.ikb_main()
    )


@dp.callback_query_handler(text="back_menu")
@dp.throttled(flood_callback, rate=1)
async def back_state(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=srart_template(),
        reply_markup=keyboard.ikb_menu(),
    )


@dp.callback_query_handler(text="poland")
@dp.throttled(flood_callback, rate=1)
async def poland_data(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Польша 🇵🇱\nВыберите пункт пропуска"),
        reply_markup=keyboard.ikb_poland(),
    )


@dp.callback_query_handler(text="lithuania")
@dp.throttled(flood_callback, rate=1)
async def lithuania_data(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nВыберите пункт пропуска"),
        reply_markup=keyboard.ikb_lithuania(),
    )


@dp.callback_query_handler(text="latvia")
@dp.throttled(flood_callback, rate=1)
async def latvia_data(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nВыберите пункт пропуска"),
        reply_markup=keyboard.ikb_latvia(),
    )


@dp.callback_query_handler(text="back_state")
@dp.throttled(flood_callback, rate=1)
async def checkpoint_back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Выберите границу с нужным государством"),
        reply_markup=keyboard.ikb_main(),
    )


@dp.callback_query_handler(text="back_help")
@dp.throttled(flood_callback, rate=1)
async def back_help(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Главное меню"), reply_markup=keyboard.ikb_menu()
    )


@dp.callback_query_handler(text="tiket")
@dp.throttled(flood_callback, rate=1)
async def tiket(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=help_template(),
    )
