from aiogram import types
from queue_bot.bot import dp
from queue_bot import keyboard
from queue_bot.utils.anti_flod import flood_callback
from queue_bot.base.template import srart_template, monitoring_template
from aiogram.dispatcher import FSMContext
from queue_bot.base.monitoring import AddMonitoring, SaveMonitoring
from queue_bot.middleware import _


@dp.message_handler(text=["Главное меню", "Main menu", "Menu główne"])
async def back_menu(message: types.Message):
    await message.answer(
        text=_(
            "Мониторинг работает неккоректно?\n/tiket - отправьте сообщение об ошибке в группу поддержки"
        ),
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await message.answer(text=srart_template(), reply_markup=keyboard.ikb_menu())


@dp.callback_query_handler(text="monitoring")
@dp.throttled(flood_callback, rate=1)
async def monitoring(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Меню управления мониторингом"), reply_markup=keyboard.ikb_monitoring()
    )


@dp.callback_query_handler(text="back_monitoring")
@dp.throttled(flood_callback, rate=1)
async def back_monitoring(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(
        text=_("Меню управления мониторингом"), reply_markup=keyboard.ikb_monitoring()
    )


@dp.callback_query_handler(text="help_monitoring")
@dp.throttled(flood_callback, rate=1)
async def help_monitoring(callback: types.CallbackQuery):
    await callback.answer(text=monitoring_template(), show_alert=True)


@dp.callback_query_handler(text="add_m")
@dp.throttled(flood_callback, rate=1)
async def add_monitoring(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_monitoring()
    await callback.message.edit_text(
        text=monitoring.response, reply_markup=monitoring.transport
    )


@dp.callback_query_handler(text="bus_monitoring")
@dp.throttled(flood_callback, rate=1)
async def bus_monitoring(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_transport(1, _("🚌 Автобус 🚌"), state)
    await callback.message.edit_text(
        text=monitoring.response, reply_markup=keyboard.ikb_monitoring_intensity()
    )


@dp.callback_query_handler(text="passenger_monitoring")
@dp.throttled(flood_callback, rate=1)
async def passenger_monitoring(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_transport(2, _("🚘 Легковой 🚘"), state)
    await callback.message.edit_text(
        text=monitoring.response, reply_markup=keyboard.ikb_monitoring_intensity()
    )


@dp.callback_query_handler(text="cargo_monitoring")
@dp.throttled(flood_callback, rate=1)
async def cargo_monitoring(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_transport(3, _("🚛 Грузовой 🚛"), state)
    await callback.message.edit_text(
        text=monitoring.response, reply_markup=keyboard.ikb_monitoring_intensity()
    )


@dp.callback_query_handler(text="intensity_1")
@dp.throttled(flood_callback, rate=1)
async def intensity_1(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_intensity(1, state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_monitoring_conf(),
        parse_mode="html",
    )


@dp.callback_query_handler(text="intensity_5")
@dp.throttled(flood_callback, rate=1)
async def intensity_5(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_intensity(5, state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_monitoring_conf(),
        parse_mode="html",
    )


@dp.callback_query_handler(text="intensity_10")
@dp.throttled(flood_callback, rate=1)
async def intensity_10(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_intensity(10, state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_monitoring_conf(),
        parse_mode="html",
    )


@dp.callback_query_handler(text="intensity_20")
@dp.throttled(flood_callback, rate=1)
async def intensity_20(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_intensity(20, state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_monitoring_conf(),
        parse_mode="html",
    )


@dp.callback_query_handler(text="intensity_50")
@dp.throttled(flood_callback, rate=1)
async def intensity_50(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = AddMonitoring(user_id)
    await monitoring.add_intensity(50, state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_monitoring_conf(),
        parse_mode="html",
    )


@dp.callback_query_handler(text="reg_m")
@dp.throttled(flood_callback, rate=1)
async def reg_monitoring(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    monitoring = SaveMonitoring(user_id)
    await monitoring.save(state)
    await callback.message.edit_text(
        text=monitoring.response,
        reply_markup=keyboard.ikb_back_monitoring(),
        parse_mode="html",
    )
    return monitoring._model


@dp.callback_query_handler(text="close_m")
@dp.throttled(flood_callback, rate=1)
async def close_monitoring(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    monitoring = SaveMonitoring(user_id)
    await monitoring.delete()
    await callback.message.edit_text(
        text=monitoring.response, reply_markup=keyboard.ikb_monitoring()
    )
