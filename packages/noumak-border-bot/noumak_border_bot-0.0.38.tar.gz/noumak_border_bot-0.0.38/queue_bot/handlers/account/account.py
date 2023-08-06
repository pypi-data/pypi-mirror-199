from aiogram import types
from queue_bot.bot import dp
from queue_bot import keyboard
from queue_bot.base.account import NumberValid
from aiogram.dispatcher import FSMContext
from queue_bot.utils.anti_flod import flood_callback
from queue_bot.base.account import Account
from queue_bot.base.account import ClientStateGroup
from queue_bot.middleware import _


@dp.callback_query_handler(text="lk")
@dp.throttled(flood_callback, rate=1)
async def lk(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=_("Личный кабинет"), reply_markup=keyboard.ikb_lk()
    )


@dp.callback_query_handler(text="back_lk")
@dp.throttled(flood_callback, rate=1)
async def back_lk(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(
        text=_("Личный кабинет"), reply_markup=keyboard.ikb_lk()
    )


@dp.callback_query_handler(text="edit_number")
@dp.throttled(flood_callback, rate=1)
async def edit_number(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.edit_number()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )


@dp.callback_query_handler(text="edit_bus")
@dp.throttled(flood_callback, rate=1)
async def edit_bus(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.edit_bus():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.edit_bus)
async def edit_number_bus(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "bus", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Номер успешно изменен"), reply_markup=keyboard.ikb_lk_back()
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="edit_passenger")
@dp.throttled(flood_callback, rate=1)
async def edit_passenger(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.edit_passenger():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.edit_car)
async def edit_number_passenger(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "car", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Номер успешно изменен"), reply_markup=keyboard.ikb_lk_back()
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="edit_cargo")
@dp.throttled(flood_callback, rate=1)
async def edit_cargo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.edit_cargo():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.edit_truck)
async def edit_number_cargo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "truck", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Номер успешно изменен"), reply_markup=keyboard.ikb_lk_back()
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="add_number")
@dp.throttled(flood_callback, rate=1)
async def add_number(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.add_number()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )


@dp.callback_query_handler(text="add_bus")
@dp.throttled(flood_callback, rate=1)
async def add_bus(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.add_bus():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.add_bus)
async def add_number_bus(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "bus", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Теперь вы отслеживаете автобус с номером: '{}' ✅").format(number),
            reply_markup=keyboard.ikb_lk_back(),
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="add_passenger")
@dp.throttled(flood_callback, rate=1)
async def add_passenger(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.add_passenger():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.add_car)
async def add_number_passenger(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "car", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Теперь вы отслеживаете авто с номером: '{}' ✅").format(number),
            reply_markup=keyboard.ikb_lk_back(),
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="add_cargo")
@dp.throttled(flood_callback, rate=1)
async def add_cargo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    if await account.add_cargo():
        await callback.message.edit_text(
            text=account.response,
        )
    else:
        await callback.message.edit_text(
            text=account.response, reply_markup=account.keyboard()
        )


@dp.message_handler(state=ClientStateGroup.add_truck)
async def add_number_cargo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data({"number": message.text})
    num = (await state.get_data("number"))["number"]
    number = NumberValid(num, state, "truck", user_id)
    if number.is_valid():
        await number.save()
        await message.answer(
            text=_("Теперь вы отслеживаете грузовую с номером: '{}' ✅").format(number),
            reply_markup=keyboard.ikb_lk_back(),
        )
    else:
        await message.answer(
            text=number.response,
        )


@dp.callback_query_handler(text="del_number")
@dp.throttled(flood_callback, rate=1)
async def del_number(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.del_number()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )


@dp.callback_query_handler(text="del_bus")
@dp.throttled(flood_callback, rate=1)
async def del_bus(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.del_bus()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )
    return account.numbers


@dp.callback_query_handler(text="del_passenger")
@dp.throttled(flood_callback, rate=1)
async def del_passenger(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.del_passenger()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )
    return account.numbers


@dp.callback_query_handler(text="del_cargo")
@dp.throttled(flood_callback, rate=1)
async def del_cargo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.del_cargo()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )
    return account.numbers


@dp.callback_query_handler(text="show_number")
@dp.throttled(flood_callback, rate=1)
async def show_number(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.show_number()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard(), parse_mode="html"
    )


@dp.callback_query_handler(text="del_numbers")
@dp.throttled(flood_callback, rate=1)
async def del_numbers(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    account = Account(user_id)
    await account.del_numbers()
    await callback.message.edit_text(
        text=account.response, reply_markup=account.keyboard()
    )
