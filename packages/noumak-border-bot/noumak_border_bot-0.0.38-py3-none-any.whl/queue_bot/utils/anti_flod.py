from queue_bot import keyboard
from aiogram.types import callback_query
from queue_bot.middleware import _


async def flood_commands(*args, **kwargs):
    update = args[0]
    await update.answer(
        text=_("Не отправляйте команды слишком часто"),
        reply_markup=keyboard.ikb_back_help(),
    )


async def flood_callback(*args, **kwargs):
    callback: callback_query = args[0]
