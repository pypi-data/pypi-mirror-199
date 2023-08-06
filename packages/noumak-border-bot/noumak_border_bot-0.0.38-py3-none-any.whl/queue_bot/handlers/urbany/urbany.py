from aiogram import types
from queue_bot.bot import dp
from queue_bot import keyboard
from queue_bot.base.parser import BusParser, PassengerParser, CargoParser
from queue_bot.utils.anti_flod import flood_callback
from queue_bot.middleware import _


@dp.callback_query_handler(text="urbany")
@dp.throttled(flood_callback, rate=1)
async def urbany_data(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны"),
        reply_markup=keyboard.ikb_urbany_ts(),
    )


@dp.callback_query_handler(text="back_urbany")
@dp.throttled(flood_callback, rate=1)
async def back_urbany(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nВыберите пункт пропуска"),
        reply_markup=keyboard.ikb_latvia(),
    )


@dp.callback_query_handler(text="urbany_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_bus(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны\nТранспорт: Автобус 🚌"),
        reply_markup=keyboard.ikb_urbany_bus(),
    )


@dp.callback_query_handler(text="back_urbany_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_back_bus(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны"),
        reply_markup=keyboard.ikb_urbany_ts(),
    )


@dp.callback_query_handler(text="urbany_place_in_queue_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_place_in_queue_bus(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = BusParser("Урбаны")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_bus()
    )

    return checkpoint_info._model


@dp.callback_query_handler(text="urbany_queue_len_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_queue_len_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Урбаны")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_bus()
    )


@dp.callback_query_handler(text="urbany_an_hour_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_hour_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Урбаны")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_bus(),
    )


@dp.callback_query_handler(text="urbany_an_day_bus")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_day_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Урбаны")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_bus(),
    )


@dp.callback_query_handler(text="urbany_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_passenger(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны\nТранспорт: Легковой 🚘"),
        reply_markup=keyboard.ikb_urbany_passenger(),
    )


@dp.callback_query_handler(text="back_urbany_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_back_passenger(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны"),
        reply_markup=keyboard.ikb_urbany_ts(),
    )


@dp.callback_query_handler(text="urbany_place_in_queue_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_place_in_queue_passenger(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = PassengerParser("Урбаны")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_passenger()
    )
    return checkpoint_info._model


@dp.callback_query_handler(text="urbany_queue_len_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_queue_len_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Урбаны")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_passenger()
    )


@dp.callback_query_handler(text="urbany_an_hour_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_hour_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Урбаны")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_passenger(),
    )


@dp.callback_query_handler(text="urbany_an_day_passenger")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_day_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Урбаны")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_passenger(),
    )


@dp.callback_query_handler(text="urbany_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_cargo(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны\nТранспорт: Грузовой  🚛"),
        reply_markup=keyboard.ikb_urbany_cargo(),
    )


@dp.callback_query_handler(text="back_urbany_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_back_cargo(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Латвия 🇱🇻\nПункт пропуска: Урбаны"),
        reply_markup=keyboard.ikb_urbany_ts(),
    )


@dp.callback_query_handler(text="urbany_place_in_queue_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_place_in_queue_cargo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = CargoParser("Урбаны")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_cargo()
    )

    return checkpoint_info._model


@dp.callback_query_handler(text="urbany_queue_len_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_queue_len_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Урбаны")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_urbany_cargo()
    )


@dp.callback_query_handler(text="urbany_an_hour_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_hour_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Урбаны")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_cargo(),
    )


@dp.callback_query_handler(text="urbany_an_day_cargo")
@dp.throttled(flood_callback, rate=1)
async def urbany_an_day_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Урбаны")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_urbany_cargo(),
    )
