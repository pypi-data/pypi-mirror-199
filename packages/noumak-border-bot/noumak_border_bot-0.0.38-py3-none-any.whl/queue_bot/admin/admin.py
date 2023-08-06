from queue_bot.bot import dp, bot
from aiogram import types
from queue_bot.settings.conf import admin_id
from queue_bot.db.models import User
from queue_bot.admin.states import AdminStates
from queue_bot import keyboard
from aiogram.dispatcher import FSMContext
from tortoise.exceptions import DoesNotExist


@dp.message_handler(commands=["admin"])
async def send_all(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text="Панель администратора",
        reply_markup=keyboard.ikb_admin(),
    )


@dp.callback_query_handler(text="mailing", state=None)
async def maliing(callback: types.CallbackQuery):
    await AdminStates.text_mailing.set()
    await callback.message.answer(
        text="Введите сообщение для рассылки, для отмены введите 'СТОП'",
    )
    await bot.answer_callback_query(callback_query_id=callback.id)


@dp.message_handler(state=AdminStates.text_mailing)
async def maliing_(message: types.Message, state: FSMContext):
    if message.text == "СТОП":
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            text="Панель администратора",
            reply_markup=keyboard.ikb_admin(),
        )
        return
    tour = await User.filter().all()
    for user in tour:
        await bot.send_message(user.telegram_id, message.text)


@dp.callback_query_handler(text="admin_add", state=None)
async def admin_add(callback: types.CallbackQuery):
    if str(callback.from_user.id) == admin_id:
        await AdminStates.admin_add.set()
        await callback.message.answer(
            text="Введите телеграм-ид пользователя, для отмены введите 'СТОП'",
        )

    else:
        await callback.message.answer(
            text="У вас нет прав",
        )
    await bot.answer_callback_query(callback_query_id=callback.id)


@dp.message_handler(state=AdminStates.admin_add)
async def admin_add_(message: types.Message, state: FSMContext):
    if message.text == "СТОП":
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            text="Панель администратора",
            reply_markup=keyboard.ikb_admin(),
        )
        return
    await state.finish()
    try:
        user = await User.get(telegram_id=message.text)
    except DoesNotExist:
        await message.answer(
            text="Данный пользователь не пользуется ботом",
            reply_markup=keyboard.ikb_admin(),
        )
    else:
        if not user.is_staff:
            user.is_staff = True
            await user.save()
            await message.answer(
                text=f"Пользователь {user.first_name} получил права администратора"
            )
        else:
            await message.answer(
                text=f"Пользователь {user.first_name} является администратором"
            )
