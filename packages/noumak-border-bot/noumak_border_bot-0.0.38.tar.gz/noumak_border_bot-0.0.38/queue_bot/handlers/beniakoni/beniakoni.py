from aiogram import types
from queue_bot.bot import dp
from queue_bot import keyboard
from queue_bot.base.parser import BusParser, PassengerParser, CargoParser
from queue_bot.utils.anti_flod import flood_callback
from queue_bot.middleware import _


@dp.callback_query_handler(text="beniakoni")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_data(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони"),
        reply_markup=keyboard.ikb_beniakoni_ts(),
    )


@dp.callback_query_handler(text="back_beniakoni")
@dp.throttled(flood_callback, rate=1)
async def back_beniakoni(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nВыберите пункт пропуска"),
        reply_markup=keyboard.ikb_lithuania(),
    )


@dp.callback_query_handler(text="beniakoni_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_bus(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони\nТранспорт: Автобус 🚌"),
        reply_markup=keyboard.ikb_beniakoni_bus(),
    )


@dp.callback_query_handler(text="back_beniakoni_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_back_bus(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони"),
        reply_markup=keyboard.ikb_beniakoni_ts(),
    )


@dp.callback_query_handler(text="beniakoni_place_in_queue_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_place_in_queue_bus(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = BusParser("Бенякони")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_beniakoni_bus()
    )

    return checkpoint_info._model


@dp.callback_query_handler(text="beniakoni_queue_len_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_queue_len_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Бенякони")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_beniakoni_bus()
    )


@dp.callback_query_handler(text="beniakoni_an_hour_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_hour_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Бенякони")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_bus(),
    )


@dp.callback_query_handler(text="beniakoni_an_day_bus")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_day_bus(callback: types.CallbackQuery):
    checkpoint_info = BusParser("Бенякони")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_bus(),
    )


@dp.callback_query_handler(text="beniakoni_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_passenger(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони\nТранспорт: Легковой 🚘"),
        reply_markup=keyboard.ikb_beniakoni_passenger(),
    )


@dp.callback_query_handler(text="back_beniakoni_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_back_passenger(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони"),
        reply_markup=keyboard.ikb_beniakoni_ts(),
    )


@dp.callback_query_handler(text="beniakoni_place_in_queue_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_place_in_queue_passenger(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = PassengerParser("Бенякони")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_passenger(),
    )

    return checkpoint_info._model


@dp.callback_query_handler(text="beniakoni_queue_len_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_queue_len_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Бенякони")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_passenger(),
    )


@dp.callback_query_handler(text="beniakoni_an_hour_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_hour_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Бенякони")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_passenger(),
    )


@dp.callback_query_handler(text="beniakoni_an_day_passenger")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_day_passenger(callback: types.CallbackQuery):
    checkpoint_info = PassengerParser("Бенякони")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_passenger(),
    )


@dp.callback_query_handler(text="beniakoni_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_cargo(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони\nТранспорт: Грузовой  🚛"),
        reply_markup=keyboard.ikb_beniakoni_cargo(),
    )


@dp.callback_query_handler(text="back_beniakoni_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_back_cargo(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Страна: Литва 🇱🇹\nПункт пропуска: Бенякони"),
        reply_markup=keyboard.ikb_beniakoni_ts(),
    )


@dp.callback_query_handler(text="beniakoni_place_in_queue_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_place_in_queue_cargo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    checkpoint_info = CargoParser("Бенякони")
    await checkpoint_info.get_place(user_id)
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_beniakoni_cargo()
    )

    return checkpoint_info._model


@dp.callback_query_handler(text="beniakoni_queue_len_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_queue_len_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Бенякони")
    await checkpoint_info.len_queue()
    await callback.message.edit_text(
        text=checkpoint_info.response, reply_markup=keyboard.ikb_beniakoni_cargo()
    )


@dp.callback_query_handler(text="beniakoni_an_hour_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_hour_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Бенякони")
    await checkpoint_info.queue_promotion_per_hour()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_cargo(),
    )


@dp.callback_query_handler(text="beniakoni_an_day_cargo")
@dp.throttled(flood_callback, rate=1)
async def beniakoni_an_day_cargo(callback: types.CallbackQuery):
    checkpoint_info = CargoParser("Бенякони")
    await checkpoint_info.queue_promotion_per_day()
    await callback.message.edit_text(
        text=checkpoint_info.response,
        reply_markup=keyboard.ikb_beniakoni_cargo(),
    )
